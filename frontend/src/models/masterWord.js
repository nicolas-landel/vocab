import { Model } from 'pinia-orm'
import { Domain } from './domain'
import { Translation } from './translation'

export class MasterWord extends Model {
  static entity = 'master_words'

  static fields() {
    return {
      id: this.uid(),
      concept: this.string(''),
      domainId: this.number(null),
      difficulty: this.string(''),
      wordType: this.string(null).nullable(),
      imageUrl: this.string(null).nullable(),
      createdAt: this.string(''),
      updatedAt: this.string(''),
      
      // Relationships
      domain: this.belongsTo(Domain, 'domainId'),
      translations: this.hasMany(Translation, 'masterWordId')
    }
  }
}