import { Model } from 'pinia-orm'
import { Domain } from './domain'
import { Translation } from './translation'

export class MasterWord extends Model {
  static entity = 'master_words'
  static primaryKey = 'concept'

  static fields() {
    return {
      concept: this.string(''),
      domainCode: this.string(''),
      difficulty: this.string(''),
      wordType: this.string(null).nullable(),
      imageUrl: this.string(null).nullable(),
      createdAt: this.string(''),
      updatedAt: this.string(''),
      
      // Relationships
      domain: this.belongsTo(Domain, 'domainCode'),
      translations: this.hasMany(Translation, 'masterWordConcept')
    }
  }
}