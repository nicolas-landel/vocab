import { Model } from 'pinia-orm'

export class User extends Model {
  static entity = 'users'

  static fields() {
    return {
      id: this.uid(),
      email: this.string(''),
      isActive: this.boolean(true),
      nativeLanguage: this.string(""),
      learningLanguages: this.attr([]),
      createdAt: this.string(''),
      updatedAt: this.string('')
    }
  }
}
