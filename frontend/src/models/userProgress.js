import { Model } from 'pinia-orm'
import { User } from './user'
import { Translation } from './translation'

export class UserProgress extends Model {
  static entity = 'user_progress'

  static fields() {
    return {
      id: this.uid(),
      userId: this.number(null),
      translationId: this.number(null),
      correctCount: this.number(0),
      incorrectCount: this.number(0),
      lastReviewed: this.string(''),
      createdAt: this.string(''),
      updatedAt: this.string(''),
      
      // Relationships
      user: this.belongsTo(User, 'userId'),
      translation: this.belongsTo(Translation, 'translationId')
    }
  }
}
