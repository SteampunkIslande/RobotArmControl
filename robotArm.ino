
#include "Braccio.h"

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

void setup()
{
    Serial.begin(115200);
    Braccio.begin();
}


void loop()
{
    if (Serial.available() > 0)
    {
        String m1S(Serial.readStringUntil(';'));
        String m2S(Serial.readStringUntil(';'));
        String m3S(Serial.readStringUntil(';'));
        String m4S(Serial.readStringUntil(';'));
        String m5S(Serial.readStringUntil(';'));
        String m6S(Serial.readStringUntil('\n'));
        Braccio.ServoMovement(10, m1S.toInt(),
                              m2S.toInt(),
                              m3S.toInt(),
                              m4S.toInt(),
                              m5S.toInt(),
                              m6S.toInt());
    }
}
