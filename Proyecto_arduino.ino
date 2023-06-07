#include <Servo.h>
#include "Adafruit_VL53L0X.h"
#include "I2Cdev.h"
#include "Wire.h"
// Dato de entrada: [selector, motor1, motor2, eje1, eje2, eje3, eje4]

// Sensor milimetrico
Adafruit_VL53L0X lox = Adafruit_VL53L0X();

// Sensores ultra sonido
const int EchoPin1 = 4;
const int TriggerPin1 = 5;
// Pines Chasis
#define Encoder1_output_A 44 // 2NARANJA
#define Encoder1_output_B 2 // 4VERDE
#define Encoder2_output_A 46 // 3NARANJA
#define Encoder2_output_B 3 // 5VERDE
const int pinENA1 = 12; //12; //13
const int pinIN1 = 23; //51;  //12
const int pinIN2 = 25; //49;  //11
const int pinENA2 = 13; //13; //8
const int pinIN3 = 27; //45; //10
const int pinIN4 = 29; //47; //9

// Variables chasis
float Count1_pulses = 0;
float Count2_pulses = 0;
float Grados1_anteriores = 0;
float Grados2_anteriores = 0;
float Grados1_actuales = 0;
float Grados2_actuales = 0;
float pulsos1 = 0;
float pulsos2 = 0;
int i = 0;
int pwm = 0;      //velocidad de giro 80% (200/255)

unsigned long TiempoInicial = 0;
unsigned long TiempoFinal = 0;

// Variables generales
int anular = 0;
int k = 0;

// Pines Brazo
#define Servo1_pin 8 // PWM
#define Servo2_pin 9 // PWM
#define Servo3_pin 10 // PWM
#define Servo4_pin 11 // PWM
Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;

// Variable brazo
int inicial1 = 45;
int inicial2 = 45;
int inicial3 = 45;
int inicial4 = 45;



// Funciones chasis --------------------------------------------------------------
void DC_Motor_Encoder1() {
  int b1 = digitalRead(Encoder1_output_B);
  if (b1 > 0) {
     Count1_pulses++;
  }
  else {
    Count1_pulses--;
  }
}

void DC_Motor_Encoder2() {
  int b2 = digitalRead(Encoder2_output_B);
  if (b2 > 0) {
    Count2_pulses++;
  }
  else {
    Count2_pulses--;
  }
}

// Funciones sensores --------------------------------------------------------
int ping(int TriggerPin, int EchoPin) {
  long duration, distanceCm;

  digitalWrite(TriggerPin, LOW);  //para generar un pulso limpio ponemos a LOW 4us
  delayMicroseconds(4);
  digitalWrite(TriggerPin, HIGH);  //generamos Trigger (disparo) de 10us
  delayMicroseconds(10);
  digitalWrite(TriggerPin, LOW);

  duration = pulseIn(EchoPin, HIGH);  //medimos el tiempo entre pulsos, en microsegundos

  distanceCm = duration * 10 / 292 / 2;  //convertimos a distancia, en cm
  return distanceCm;
}

// Funciones generales --------------------------------------------------------


void setup()
{
  // Protocolos de comunicacion
  Serial.begin(230400);
  // Chasis
  pinMode(pinIN1, OUTPUT);
  pinMode(pinIN2, OUTPUT);
  pinMode(pinENA1, OUTPUT);
  pinMode(pinIN3, OUTPUT);
  pinMode(pinIN4, OUTPUT);
  pinMode(pinENA2, OUTPUT);
  pinMode(Encoder1_output_A, INPUT); // sets the Encoder_output_A pin as the input
  pinMode(Encoder1_output_B, INPUT); // sets the Encoder_output_B pin as the input
  attachInterrupt(digitalPinToInterrupt(Encoder1_output_A), DC_Motor_Encoder1, RISING);
  pinMode(Encoder2_output_A, INPUT); // sets the Encoder_output_A pin as the input
  pinMode(Encoder2_output_B, INPUT); // sets the Encoder_output_B pin as the input
  attachInterrupt(digitalPinToInterrupt(Encoder2_output_A), DC_Motor_Encoder2, RISING);
  // Brazo
  motor1.attach(Servo1_pin);
  motor2.attach(Servo2_pin);
  motor3.attach(Servo3_pin);
  motor4.attach(Servo4_pin);
  motor1.write(inicial1);
  motor2.write(inicial2);
  motor3.write(inicial3);
  motor4.write(inicial4);
  //Sensores ultrasonido
  pinMode(TriggerPin1, OUTPUT);
  pinMode(EchoPin1, INPUT);
  // Sensor mega preciso
  if (!lox.begin()) {
    Serial.println(F("Error al iniciar VL53L0X"));
    while (1);
  }
  // Variable de tiempo
  TiempoInicial = millis();
}

void loop() {

  if (Serial.available() > 0) {
    // Read the incoming string
    String integer_string = Serial.readStringUntil('\n');
    int integer_array[6]; //motor1, motor2, Servo1, servo2, servo3, servo4
    int i = 0;
    char* token = strtok((char*)integer_string.c_str(), ",");
    while (token != NULL && i < 6) {
      integer_array[i] = atoi(token);
      i++;
      token = strtok(NULL, ",");
    }
    if (integer_array[0] == 1) { // MOVER CHASIS
      Serial.println("Motores");
      if ((integer_array[1] == 0) && (integer_array[2] == 0 )) {
        if (anular == 1) {
          Count1_pulses = 0;
        }
        else if (anular == 2) {
          Count2_pulses = 0;
        }
        digitalWrite(pinIN1, LOW);
        digitalWrite(pinIN2, LOW);
        analogWrite(pinENA1, 0);
        digitalWrite(pinIN3, LOW);
        digitalWrite(pinIN4, LOW);
        analogWrite(pinENA2, 0);
        anular = 0;
        }
      else if (integer_array[1] > 0 ) { //Si el comando es "on"
        //Serial.println("1");
        digitalWrite(pinIN1, LOW);
        digitalWrite(pinIN2, HIGH);
        analogWrite(pinENA1, 200);
        digitalWrite(pinIN3, LOW);
        digitalWrite(pinIN4, HIGH);
        analogWrite(pinENA2, 200);
        Serial.println("Avanzando");
      }
      else if (integer_array[1] < 0 ) {
        //Serial.println("2");
        digitalWrite(pinIN1, HIGH);
        digitalWrite(pinIN2, LOW);
        analogWrite(pinENA1, 150);
        digitalWrite(pinIN3, HIGH);
        digitalWrite(pinIN4, LOW);
        analogWrite(pinENA2, 200);
        Serial.println("Retrocediendo");

      }
      else if (integer_array[2] > 0 ) { // Funciona
        anular = 2;
        digitalWrite(pinIN1, LOW);
        digitalWrite(pinIN2, LOW);
        analogWrite(pinENA1, 0);
        digitalWrite(pinIN3, LOW);
        digitalWrite(pinIN4, HIGH);
        analogWrite(pinENA2, 200);
        Serial.println("Derecha");
      }
      else if (integer_array[2] < 0 ) {
        anular = 1;
        digitalWrite(pinIN1, LOW);
        digitalWrite(pinIN2, HIGH);
        analogWrite(pinENA1, 200);
        digitalWrite(pinIN3, LOW);
        digitalWrite(pinIN4, LOW);
        analogWrite(pinENA2, 0);
        Serial.println("Izquierda");
      }
    }

    if (integer_array[0] == 2) { // Mover brazo
      motor1.write(integer_array[3]);
      motor2.write(integer_array[4]);
      motor3.write(integer_array[5]);
      motor4.write(integer_array[6]);
      Serial.println("Brazo");
    }

  }
  i = 0;
  
  pulsos1 = Count1_pulses;
  pulsos2 = Count2_pulses;
  Grados1_actuales = pulsos1 * 360.0 / 77.0;
  Grados2_actuales = pulsos2 * 360.0 / 77.0;
  //int cm1 = 0;
  //int cm2 = 0;
  //int cm3 = 0;
  int cm1 = ping(TriggerPin1, EchoPin1);// Esto hace que todo se demore
  VL53L0X_RangingMeasurementData_t measure;
  lox.rangingTest(&measure, false); // si se pasa true como parametro, muestra por puerto serie datos de debug
  
  TiempoFinal = millis();
  if ((TiempoFinal - TiempoInicial) > 100) {
    Serial.print(k);
    Serial.print(",");
    Serial.print(String(Grados1_actuales));
    Serial.print(",");
    Serial.print(String(Grados2_actuales));
    Serial.print(",");
    Serial.print(motor1.read());
    Serial.print(",");
    Serial.print(motor2.read());
    Serial.print(",");
    Serial.print(motor3.read());
    Serial.print(",");
    Serial.print(motor4.read());
    Serial.print(",");

    if (measure.RangeStatus != 4)
    {
      Serial.print(measure.RangeMilliMeter);
    }
    else {
      Serial.print(2000); // Valor muy grande si esta fuera del rango
    }
    Serial.print(",");
    Serial.print(cm1); // Lectura sensores ultrasonido
    Serial.print(",");
    Serial.println(String(TiempoFinal - TiempoInicial));
    Count1_pulses = 0;
    Count2_pulses = 0;
    TiempoInicial = 0;
    TiempoFinal = 0;
    Grados1_actuales = 0;
    Grados2_actuales = 0;
    TiempoInicial = millis();
    k = k + 1;
  }

  //delay(100);
  //Serial.flush();
}