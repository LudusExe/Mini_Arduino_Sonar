// ===============================
// LUDUS SONAR - Arduino Radar GUI
// ===============================
// Versione migliorata di Indian Lifehacker Radar
// Ottimizzato da ChatGPT
// ===============================

import processing.serial.*; 
import java.awt.event.KeyEvent; 
import java.io.IOException;

Serial myPort;

// Variabili dati
String angle = "";
String distance = "";
String data = "";
String noObject;
float pixsDistance;
int iAngle, iDistance;
int index1 = 0;
int index2 = 0;

PFont orcFont;

void setup() {
  size(1200, 700); // Modifica a piacere in base alla risoluzione dello schermo
  smooth();

  println(Serial.list()); // Mostra le porte disponibili
  // 🔧 Cambia "COM3" con la tua porta corretta
  myPort = new Serial(this, "COM3", 9600); 
  myPort.bufferUntil('.');
}

void draw() {
  // Effetto scia e sfondo
  noStroke();
  fill(0, 4); 
  rect(0, 0, width, height - height * 0.065);

  fill(98, 245, 31); // Verde radar
  drawRadar(); 
  drawLine();
  drawObject();
  drawText();
}

// ===========================================
// 📡 Gestione dei dati seriali da Arduino
// ===========================================
void serialEvent(Serial myPort) {
  try {
    data = myPort.readStringUntil('.');
    if (data == null) return;
    data = trim(data.substring(0, data.length() - 1));

    index1 = data.indexOf(",");
    if (index1 <= 0) return;

    angle = data.substring(0, index1);
    distance = data.substring(index1 + 1);

    iAngle = int(angle);
    iDistance = int(distance);
  } 
  catch (Exception e) {
    println("Errore nella lettura seriale: " + e.getMessage());
  }
}

// ===========================================
// 🎯 Disegno radar e componenti grafiche
// ===========================================
void drawRadar() {
  pushMatrix();
  translate(width / 2, height - height * 0.074);
  noFill();
  strokeWeight(2);
  stroke(98, 245, 31);

  // Cerchi concentrici
  for (int i = 1; i <= 4; i++) {
    float r = (width - width * (0.0625 + (i - 1) * 0.208)) ;
    arc(0, 0, r, r, PI, TWO_PI);
  }

  // Linee angolari
  for (int a = 0; a <= 150; a += 30) {
    line(0, 0, (-width / 2) * cos(radians(a)), (-width / 2) * sin(radians(a)));
  }

  line(-width/2, 0, width/2, 0); // Linea orizzontale
  popMatrix();
}

void drawObject() {
  pushMatrix();
  translate(width / 2, height - height * 0.074);
  strokeWeight(9);
  stroke(255, 10, 10); // Rosso per oggetto

  pixsDistance = iDistance * ((height - height * 0.1666) * 0.025);
  
  // Mostra solo se entro 40 cm
  if (iDistance < 40) {
    line(pixsDistance * cos(radians(iAngle)), 
         -pixsDistance * sin(radians(iAngle)), 
         (width - width * 0.505) * cos(radians(iAngle)), 
         -(width - width * 0.505) * sin(radians(iAngle)));
  }
  popMatrix();
}

void drawLine() {
  pushMatrix();
  strokeWeight(9);
  stroke(30, 250, 60);
  translate(width / 2, height - height * 0.074);
  line(0, 0, 
       (height - height * 0.12) * cos(radians(iAngle)), 
       -(height - height * 0.12) * sin(radians(iAngle)));
  popMatrix();
}

// ===========================================
// 🖋️ Testo e indicatori
// ===========================================
void drawText() {
  pushMatrix();
  fill(0);
  noStroke();
  rect(0, height - height * 0.0648, width, height);
  
  fill(98, 245, 31);
  textSize(25);

  // Distanze
  text("10cm", width * 0.615, height - height * 0.0833);
  text("20cm", width * 0.719, height - height * 0.0833);
  text("30cm", width * 0.823, height - height * 0.0833);
  text("40cm", width * 0.927, height - height * 0.0833);

  // Stato
  noObject = (iDistance > 40) ? "Fuori portata" : "Oggetto rilevato";
  
  textSize(40);
  text("Ludus Sonar", width * 0.125, height - height * 0.0277);
  text("Angolo: " + iAngle + "°", width * 0.52, height - height * 0.0277);
  text("Distanza: " + (iDistance < 40 ? iDistance + " cm" : "Fuori portata"), 
       width * 0.74, height - height * 0.0277);

  // Etichette angolari
  textSize(25);
  fill(98, 245, 60);
  drawAngleLabel(30);
  drawAngleLabel(60);
  drawAngleLabel(90);
  drawAngleLabel(120);
  drawAngleLabel(150);

  popMatrix();
}

void drawAngleLabel(int angleDeg) {
  pushMatrix();
  translate(
    width / 2 + (width / 2 - width * 0.5) * cos(radians(angleDeg)),
    (height - height * 0.0833) - (width / 2) * sin(radians(angleDeg))
  );
  rotate(-radians(angleDeg - 90));
  text(angleDeg + "°", 0, 0);
  popMatrix();
}
