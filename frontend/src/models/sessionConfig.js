import { Model } from 'pinia-orm'
import { User } from './user'
import { Language } from './language'

export class SessionConfig extends Model {
  static entity = 'session_configs'

  static fields() {
    return {
      id: this.uid(),
      userId: this.string(null),
      nativeLanguage: this.string(''),
      languageTested: this.string(''),
      difficulty: this.string(null).nullable(),
      domain: this.string(null).nullable(),
      sessionType: this.string(''),
      createdAt: this.string(''),
      updatedAt: this.string(''),
      
      // Relationships
      user: this.belongsTo(User, 'userId'),
      nativeLang: this.belongsTo(Language, 'nativeLanguage', 'code'),
      testedLang: this.belongsTo(Language, 'languageTested', 'code')
    }
  }
}
