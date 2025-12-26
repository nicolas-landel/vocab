import { Model } from 'pinia-orm'

export class Domain extends Model {
  static entity = 'domains'
  static primaryKey = 'code'

  static fields() {
    return {
      name: this.string(''),
      code: this.string(''),
      createdAt: this.string(''),
      updatedAt: this.string('')
    }
  }
}
