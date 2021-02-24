#include <FastLED.h>

#define LED_PIN     3
#define NUM_LEDS    6
#define BRIGHTNESS  255
#define LED_TYPE    WS2811

CRGB Strip[NUM_LEDS];

const int Buton_1 = 11;
const int Buton_2 = 10;
const int Buton_3 = 2;
const int Buton_4 = 9;
const int Buton_5 = 12;
const int Buton_6 = 8;

const int Color_Pressed = 200 ;
const int Color_Reg = 100 ;

const float Pin [6] = {11, 10, 2, 8, 12, 9} ;
bool State [6] = {false, false, false, false, false, false} ;

int Message ;

float Time_0 ;
float Time ;
float Waited ;
const float Reg_Time = 1 ;
const int Reg_Speed_Animation = 500 ;

void setup() {
  Serial.begin(9600);
  Serial.println("Ready");
  pinMode(Buton_1, INPUT);
  pinMode(Buton_2, INPUT);
  pinMode(Buton_3, INPUT);
  pinMode(Buton_4, INPUT);
  pinMode(Buton_5, INPUT);
  pinMode(Buton_6, INPUT);

  FastLED.addLeds<WS2812B, LED_PIN>(Strip, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
}

void loop() {

  Get_State() ;
  Pressed_Sending() ;
  Receive_Check() ;
}


void Get_State(){
    State[0] = digitalRead(Buton_1);
    State[1] = digitalRead(Buton_2);
    State[2] = digitalRead(Buton_3);
    State[3] = digitalRead(Buton_4);
    State[4] = digitalRead(Buton_5);
    State[5] = digitalRead(Buton_6);
}

void Pressed_Sending(){
    for (int i = 0; i <= 5; i++) {
      if(State[i] == true){
        Time_0 = (millis())*0.001 ;
        Time_Update() ;
        while(State[i] == true and Waited < Reg_Time){
            Get_State() ;
            Time_Update() ;
        }
        if(Waited < Reg_Time){
            Pressed(i);
        }
        else{
            Register_animation(i) ;
        }
      }
    }
    FastLED.show();
}

void Receive_Check(){
    if (Serial.available()){
        Message = Serial.parseInt(); 
    }
    Serial.flush(); 
}

void Time_Update(){
    Time = (millis())*0.001 ;
    Waited = Time - Time_0 ;
    //Serial.println(Waited);
}

void Register_animation(int i){
    Receive_Check();
    while(Message != i+1 ){
        Strip[i] = CHSV(Color_Reg, 255, 255);
        delay(Reg_Speed_Animation);
        FastLED.show();
        Strip[i] = CRGB::Black ;
        delay(Reg_Speed_Animation);
        FastLED.show();
        Receive_Check();
    }
    Message = 0 ; 
}

void Pressed(int i){
    Receive_Check();
    Serial.print("P");
    Serial.println(i+1);
    
    while(Message != i+1){
            Strip[i] = CHSV(Color_Pressed, 255, 255);
            FastLED.show();
            Receive_Check();
        }
    Strip[i] = CRGB::Black ;
    FastLED.show();
    Message = 0 ;
    
    
}

//------------------------------------------------------------------------------------------------------------------------------

void Display(){
    for (int i = 0; i <= 5; i++) {
        Serial.print(State [i]) ;
        Serial.print("  |  ") ;
    }
    Serial.println(" ");
}
