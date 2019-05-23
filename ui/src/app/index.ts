import Phaser from "phaser";
import piano_sound from "../common_assets/sounds/447127__pax11__piano-pop-amajor-100bpm.wav";
import quantum_sound from "../common_assets/sounds/384468__frankum__vintage-elecro-pop-loop.mp3";
import happy_birthay_sound from "../common_assets/sounds/369147__inspectorj__music-box-happy-birthday.wav";

class GameScene2 extends Phaser.Scene {
  constructor() {
    super("SecondScene");
  }

  init() {}

  preload(): void {
    this.load.audio("quantom_sound", quantum_sound);
    this.load.audio("piano_sound", piano_sound);
    this.load.audio("happy_birthday_sound", happy_birthay_sound);
  }

  create(): void {
    let introText = "Test";
    this.add.text(20, 20, introText, { fill: "yellow" });
    this.sound.play("happy_birthday_sound");
    this.time.addEvent({
      delay: 24000,
      callback: this.wakeUpInNoWhere,
      callbackScope: this
    });

    // TODO
  }
  update(time: number, delta: number): void {
    // TODO
  }

  drawInfiniteSquare(
    x: number,
    y: number,
    width: number,
    height: number,
    primaryColor?: boolean
  ) {
    this.add
      .rectangle(x, y, width, height, primaryColor ? 0x00ff00 : 0x000000)
      .setOrigin(0, 0);
    if (width > 20 && height > 20) {
      this.time.addEvent({
        delay: 200,
        callback: () =>
          this.drawInfiniteSquare(
            x + 2,
            y + 2,
            width - 4,
            height - 4,
            !primaryColor
          ),
        callbackScope: this
      });
    } else {
      this.add.rectangle(450, 300, 100, 300, 0x00ff00).setOrigin(0, 0);
    }
  }

  wakeUpInNoWhere() {
    this.sound.stopAll();
    this.sound.play("piano_sound", { loop: true });
    this.add.text(40, 60, "Chapter 1: Real World");
    this.drawInfiniteSquare(400, 100, 200, 200);
    // Draw black square inside
  }
}

const SceneArray = new Array<Phaser.Scene>(new GameScene2());

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  physics: {
    default: "arcade",
    arcade: {
      gravity: { y: 200 }
    }
  },
  backgroundColor: 0xcccccc,
  scene: SceneArray
};

export class StarfallGame extends Phaser.Game {
  constructor(config: Phaser.Types.Core.GameConfig) {
    super(config);
  }
}

window.onload = () => {
  var game = new StarfallGame(config);
};
