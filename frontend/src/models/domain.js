import { Model } from 'pinia-orm'

export class Domain extends Model {
  static entity = 'domains'

  static fields() {
    return {
      id: this.uid(),
      name: this.string(''),
      createdAt: this.string(''),
      updatedAt: this.string('')
    }
  }
}
