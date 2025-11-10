import processing.serial.*;
import java.awt.event.KeyEvent;
import java.io.IOException;

Serial myPort;

String angle = "";
String distance = "";
String data = "";
float pixsDistance;
int iAngle, iDistance;

ArrayList<Echo> echoes = new ArrayList<Echo>();

PFont orcFont;

// Height of the bottom UI bar
float uiHeight = 60;

void setup() {
  size(1200, 700);
  smooth();

  println(Serial.list());
  // Change "COM3" to your correct serial port
  myPort = new Serial(this, "COM3", 9600);
  myPort.bufferUntil('.');

  orcFont = createFont("Consolas", 20);
  textFont(orcFont);
}

void draw() {
  fill(0, 25);
  noStroke();
  rect(0, 0, width, height);

  // Position the radar above the UI bar
  translate(width / 2, height - uiHeight - 30);

  drawRadar();
  drawBeam();
  drawEchoes();
  drawObject();
  drawUI();
}

void serialEvent(Serial myPort) {
  try {
    data = myPort.readStringUntil('.');
    if (data == null) return;

    data = trim(data.substring(0, data.length() - 1));
    int index1 = data.indexOf(",");
    if (index1 <= 0) return;

    angle = data.substring(0, index1);
    distance = data.substring(index1 + 1);

    iAngle = int(angle);
    iDistance = int(distance);

    if (iDistance < 40) {
      echoes.add(new Echo(iAngle, iDistance));
    }
  } 
  catch (Exception e) {
    println("Serial read error: " + e.getMessage());
  }
}

void drawRadar() {
  noFill();
  stroke(98, 245, 31);
  strokeWeight(2);

  float maxR = width * 0.9;

  for (int i = 1; i <= 4; i++) {
    float r = map(i, 0, 4, 0, maxR);
    arc(0, 0, r, r, PI, TWO_PI);
  }

  for (int a = 0; a <= 150; a += 30) {
    float x = (maxR / 2) * cos(radians(a));
    float y = (maxR / 2) * sin(radians(a));
    line(0, 0, -x, -y);
    drawAngleLabel(a, maxR / 2 + 30);
  }

  line(-maxR / 2, 0, maxR / 2, 0);
}

void drawBeam() {
  stroke(98, 245, 60, 180);
  strokeWeight(4);
  float r = width * 0.9 / 2;
  line(0, 0, -r * cos(radians(iAngle)), -r * sin(radians(iAngle)));

  noStroke();
  fill(98, 245, 31, 40);
  arc(0, 0, width * 0.9, width * 0.9, radians(iAngle - 2), radians(iAngle + 2));
}

void drawObject() {
  if (iDistance < 40) {
    float r = map(iDistance, 0, 40, 0, width * 0.9 / 2);
    noStroke();
    fill(255, 50, 50, 80);
    ellipse(-r * cos(radians(iAngle)), -r * sin(radians(iAngle)), 40, 40);
    fill(255, 0, 0);
    ellipse(-r * cos(radians(iAngle)), -r * sin(radians(iAngle)), 12, 12);
  }
}

void drawEchoes() {
  for (int i = echoes.size() - 1; i >= 0; i--) {
    Echo e = echoes.get(i);
    e.display();
    if (e.alpha <= 0) echoes.remove(i);
  }
}

void drawAngleLabel(int angleDeg, float r) {
  pushMatrix();
  float x = -r * cos(radians(angleDeg));
  float y = -r * sin(radians(angleDeg));
  fill(98, 245, 60);
  textAlign(CENTER, CENTER);
  text(angleDeg + "°", x, y);
  popMatrix();
}

void drawUI() {
  resetMatrix();
  fill(0);
  noStroke();
  rect(0, height - uiHeight, width, uiHeight);

  fill(98, 245, 31);
  textSize(32);
  textAlign(LEFT, CENTER);
  text("Ludus Sonar", 30, height - uiHeight / 2);

  textAlign(CENTER, CENTER);
  text("Angle: " + iAngle + "°", width / 2, height - uiHeight / 2);
  text("Distance: " + (iDistance < 40 ? iDistance + " cm" : "Out of range"), width * 0.8, height - uiHeight / 2);
}

class Echo {
  float angle, dist, alpha;
  Echo(float a, float d) {
    angle = a;
    dist = d;
    alpha = 255;
  }

  void display() {
    float r = map(dist, 0, 40, 0, width * 0.9 / 2);
    stroke(255, 0, 0, alpha);
    strokeWeight(6);
    point(-r * cos(radians(angle)), -r * sin(radians(angle)));
    alpha -= 3;
  }
}
