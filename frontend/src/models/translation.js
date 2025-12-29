import { Model } from 'pinia-orm'
import { MasterWord } from './masterWord'
import { Language } from './language'

export class Translation extends Model {
  static entity = 'translations'

  static fields() {
    return {
      id: this.uid(),
      masterWordConcept: this.string(''),
      text: this.string(''),
      languageCode: this.string(''),
      audioUrl: this.string(''),
      gender: this.string(''),
      pluralText: this.string(''),
      sentenceExample: this.string(''),
      createdAt: this.string(''),
      updatedAt: this.string(''),
      
      // User-specific data (from UserTranslation join)
      isKnown: this.boolean(false),
      
      // Relationships
      masterWord: this.belongsTo(MasterWord, 'masterWordConcept'),
      language: this.belongsTo(Language, 'languageCode', 'code')
    }
  }
}