interface Level {
  entrypoint: number;
  levelId: number;
  outpoints: Array<number>;
  name: string;
  entryname: string;
  description: string;
}

class Manager {
  private registered_levels: Array<Level>;

  constructor() {
    this.registered_levels = [];
  }

  getLevels(entryPointId: number): Array<Level> {
    /**
     * Get a list of levels matching an endpoint
     */
    let available_levels = new Array<Level>();
    for (let level of this.registered_levels) {
      if (level.entrypoint == entryPointId) {
        available_levels.push(level);
      }
    }
    return available_levels;
  }

  addLevel(level: Level): boolean {
    /**
     *  Add a level to the game.
     *  Returns false if a level with the same identifier has been already added
     */
    for (let level of this.registered_levels) {
      if (level.levelId == level.levelId) {
        return false;
      }
    }
    this.registered_levels.push(level);
    return true;
  }
}
