import { Model } from 'pinia-orm'
import { SessionConfig } from './sessionConfig'
import { User } from './user'
import { SessionWord } from './sessionWord'

export class Session extends Model {
  static entity = 'sessions'

  static fields() {
    return {
      id: this.uid(),
      configId: this.string(null),
      userId: this.string(null),
      sourceLangCode: this.string(''),
      targetLangCode: this.string(''),
      domain: this.string(''),
      difficulty: this.string(''),
      sessionType: this.string(''),
      score: this.number(null),
      completedAt: this.string(''),
      createdAt: this.string(''),
      updatedAt: this.string(''),
      
      // Relationships
      config: this.belongsTo(SessionConfig, 'configId'),
      user: this.belongsTo(User, 'userId'),
      results: this.hasMany(SessionWord, 'sessionId')
    }
  }
}
