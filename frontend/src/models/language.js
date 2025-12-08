import { Model } from 'pinia-orm'

export class Language extends Model {
  static entity = 'languages'
  static primaryKey = 'code'

  static fields() {
    return {
      code: this.string(''),
      name: this.string('')
    }
  }
}