import { Model } from 'pinia-orm'
import { Session } from './session'
import { Translation } from './translation'

export class SessionResult extends Model {
  static entity = 'session_results'

  static fields() {
    return {
      id: this.uid(),
      sessionId: this.number(null),
      translationId: this.number(null),
      correct: this.boolean(false),
      createdAt: this.string(''),
      
      // Relationships
      session: this.belongsTo(Session, 'sessionId'),
      translation: this.belongsTo(Translation, 'translationId')
    }
  }
}
