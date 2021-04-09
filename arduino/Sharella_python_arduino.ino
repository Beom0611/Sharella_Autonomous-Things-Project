#include <SoftwareSerial.h>

SoftwareSerial BTSerial(2,3);

const int ledPin = 7;                                                             // LED 7번 핀 설정



void setup()

{

  pinMode(ledPin, OUTPUT);                                                   // ledPin 을 output으로 설정

  Serial.begin(9600);

  BTSerial.begin(9600);

}



void loop()

{


  if (BTSerial.available()) {

    byte data = BTSerial.read();                                              // 블루투스 모듈에서 아두이노로 송신된 정보를 data 로 저장
                                                           

    if (data == '1') {                                                        // data = 1 이면 led 를 키고, BTSerial 과 Serial 에 'on' 입력

      digitalWrite(ledPin, HIGH);

      BTSerial.write("On");

      Serial.write("1");

    }                                                                                 

    else if (data == '0') {                                                   // data = 0 이면 led 를 끄고, BTSerial 과 Serial 에 'off' 입력

      digitalWrite(ledPin, LOW);

      BTSerial.write("Off");

      Serial.write("0");

    }                                                                                  

    else {

      BTSerial.write(" ");

    }

  }

}
