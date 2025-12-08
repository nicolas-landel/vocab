import { Model } from 'pinia-orm'



export class Word extends Model {
  static entity = 'words'

  static fields() {
    return {
      id: this.number(0),
      text: this.string(''),
      language_code: this.string(''),
      domain: this.string(''),
      difficulty: this.string('')
    }
  }
}

export class Session extends Model {
  static entity = 'sessions'

  static fields() {
    return {
      id: this.number(0),
      user_id: this.number(0),
      source_lang_code: this.string(''),
      target_lang_code: this.string(''),
      domain: this.string('').nullable(),
      difficulty: this.string('').nullable(),
      session_type: this.string(''),
      score: this.number(0).nullable(),
      results: this.hasMany(SessionResult, 'session_id')
    }
  }
}

export class SessionResult extends Model {
  static entity = 'session_results'

  static fields() {
    return {
      id: this.number(0),
      session_id: this.number(0),
      word_id: this.number(0),
      correct: this.boolean(false),
      word: this.belongsTo(Word, 'word_id')
    }
  }
}
