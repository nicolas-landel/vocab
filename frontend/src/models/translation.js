import { Model } from 'pinia-orm'
import { MasterWord } from './masterWord'
import { Language } from './language'

export class Translation extends Model {
  static entity = 'translations'

  static fields() {
    return {
      id: this.uid(),
      masterWordId: this.number(null),
      text: this.string(''),
      languageCode: this.string(''),
      audioUrl: this.string(null).nullable(),
      gender: this.string(null).nullable(),
      pluralText: this.string(null).nullable(),
      sentenceExample: this.string(null).nullable(),
      createdAt: this.string(''),
      updatedAt: this.string(''),
      
      // User-specific data (from UserTranslation join)
      isKnown: this.boolean(false),
      
      // Relationships
      masterWord: this.belongsTo(MasterWord, 'masterWordId'),
      language: this.belongsTo(Language, 'languageCode', 'code')
    }
  }
}