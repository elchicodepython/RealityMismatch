import player from "../common_assets/images/player.png";
import Phaser from "phaser";

interface PlayerKeyboard {
  up: Phaser.Input.Keyboard.Key;
  down: Phaser.Input.Keyboard.Key;
  left: Phaser.Input.Keyboard.Key;
  right: Phaser.Input.Keyboard.Key;
}

export class PlayerScene extends Phaser.Scene {
  protected player!: Phaser.GameObjects.Sprite;
  private keys!: PlayerKeyboard;
  protected playerPhisics!: Phaser.Physics.Arcade.Group;
  private startX: number;
  private startY: number;

  constructor(codename: string = "PlayerScene") {
    super(codename);
    this.startX = 8;
    this.startY = 0;
  }

  preload() {
    this.load.spritesheet("player", player, {
      frameHeight: 16,
      frameWidth: 16
    });
  }
  create() {
    this.playerPhisics = this.physics.add.group();
    this.player = this.physics.add.sprite(this.startX, this.startY, "player");
    this.player.setInteractive();
    this.playerPhisics.add(player);

    // Set player animation
    this.anims.create({
      key: "playing",
      frames: this.anims.generateFrameNames("player"),
      frameRate: 10,
      repeat: -1
    });

    this.anims.play("playing", this.player);

    // Set the keys to interact with the player
    this.keys = {
      up: this.input.keyboard.addKey("W"),
      left: this.input.keyboard.addKey("A"),
      down: this.input.keyboard.addKey("S"),
      right: this.input.keyboard.addKey("D")
    };
  }

  update() {
    this.movePlayerManager();
  }

  movePlayerManager() {
    if (this.keys.left.isDown) {
      this.playerPhisics.setVelocityX(200);
    }

    if (this.keys.right.isDown) {
    }
    if (this.keys.up.isDown) {
    }
    if (this.keys.down.isDown) {
    }
  }
}

export class BankScene extends PlayerScene {
  constructor() {
    super("BankScene");
  }

  create() {
    const floorRect = this.physics.add.sprite(200, 300, "player");
    floorRect.body.setSize(200, 30);
    floorRect.setCollideWorldBounds(true);

    //this.physics.add.existing(floorRect);

    PlayerScene.prototype.create.call(this);
  }
}
