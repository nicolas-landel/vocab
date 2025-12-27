import { Model } from 'pinia-orm'
import { User } from './user'
import { Language } from './language'

export class UserLanguage extends Model {
  static entity = 'user_languages'

  static fields() {
    return {
      id: this.uid(),
      userId: this.string(null),
      languageCode: this.string(''),
      level: this.string(''),
      isLearning: this.boolean(true),
      createdAt: this.string(''),
      updatedAt: this.string(''),
      
      // Relationships
      user: this.belongsTo(User, 'userId'),
      language: this.belongsTo(Language, 'languageCode', 'code')
    }
  }
}
    