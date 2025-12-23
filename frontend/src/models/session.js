import { Model } from 'pinia-orm'
import { SessionConfig } from './sessionConfig'
import { User } from './user'
import { SessionResult } from './sessionResult'

export class Session extends Model {
  static entity = 'sessions'

  static fields() {
    return {
      id: this.uid(),
      configId: this.number(null),
      userId: this.number(null),
      sourceLangCode: this.string(''),
      targetLangCode: this.string(''),
      domain: this.string(null).nullable(),
      difficulty: this.string(null).nullable(),
      sessionType: this.string(''),
      score: this.number(null).nullable(),
      completedAt: this.string(null).nullable(),
      createdAt: this.string(''),
      updatedAt: this.string(''),
      
      // Relationships
      config: this.belongsTo(SessionConfig, 'configId'),
      user: this.belongsTo(User, 'userId'),
      results: this.hasMany(SessionResult, 'sessionId')
    }
  }
}
