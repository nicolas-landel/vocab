import { Model } from 'pinia-orm'
import { Session } from './session'
import { Translation } from './translation'

export class SessionWord extends Model {
  static entity = 'session_words'

  static fields() {
    return {
      id: this.uid(),
      sessionId: this.string(null),
      translationFromId: this.string(null),
      translationToId: this.string(null),
      fromLanguage: this.string(''),
      toLanguage: this.string(''),
      correct: this.boolean(null),
      userAnswer: this.string(null),
      createdAt: this.string(''),
      
      // Relationships
      session: this.belongsTo(Session, 'sessionId'),
      translationTo: this.belongsTo(Translation, 'translationToId'),
      translationFrom: this.belongsTo(Translation, 'translationFromId'),
    }
  }
}
