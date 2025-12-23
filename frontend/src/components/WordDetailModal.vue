<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="600">
    <v-card v-if="translation">
      <v-card-title class="d-flex justify-space-between align-center">
        <span>{{ translation.text }}</span>
        <v-btn icon="mdi-close" variant="text" @click="$emit('update:modelValue', false)"></v-btn>
      </v-card-title>

      <v-divider></v-divider>

      <v-card-text class="pt-4">
        <v-row>
          <!-- Native Language Translation -->
          <v-col cols="12">
            <div class="text-subtitle-2 text-grey">Translation</div>
            <div class="text-h6">{{ translation.masterWord?.text || '-' }}</div>
          </v-col>

          <!-- Gender -->
          <v-col cols="6" v-if="translation.gender">
            <div class="text-subtitle-2 text-grey">Gender</div>
            <div class="text-body-1">{{ translation.gender }}</div>
          </v-col>

          <!-- Plural Form -->
          <v-col cols="6" v-if="translation.plural">
            <div class="text-subtitle-2 text-grey">Plural</div>
            <div class="text-body-1">{{ translation.plural }}</div>
          </v-col>

          <!-- Domain -->
          <v-col cols="6">
            <div class="text-subtitle-2 text-grey">Domain</div>
            <div class="text-body-1">{{ translation.masterWord?.domain?.name || '-' }}</div>
          </v-col>

          <!-- Difficulty -->
          <v-col cols="6">
            <div class="text-subtitle-2 text-grey">Difficulty</div>
            <v-chip :color="getDifficultyColor(translation.difficulty)" size="small">
              {{ translation.difficulty }}
            </v-chip>
          </v-col>

          <!-- Example Sentence -->
          <v-col cols="12" v-if="translation.exampleSentence">
            <div class="text-subtitle-2 text-grey">Example</div>
            <div class="text-body-1 font-italic">"{{ translation.exampleSentence }}"</div>
          </v-col>

          <!-- Pronunciation -->
          <v-col cols="12" v-if="translation.pronunciation">
            <div class="text-subtitle-2 text-grey">Pronunciation</div>
            <div class="text-body-1">{{ translation.pronunciation }}</div>
          </v-col>

          <!-- Audio Pronunciation -->
          <v-col cols="12" v-if="translation.audioUrl">
            <div class="text-subtitle-2 text-grey mb-2">Listen</div>
            <audio controls :src="translation.audioUrl" class="w-100"></audio>
          </v-col>

          <!-- Synonyms -->
          <v-col cols="12" v-if="translation.synonyms && translation.synonyms.length > 0">
            <div class="text-subtitle-2 text-grey mb-2">Synonyms</div>
            <v-chip-group>
              <v-chip
                v-for="(synonym, index) in translation.synonyms"
                :key="index"
                size="small"
                variant="outlined"
              >
                {{ synonym }}
              </v-chip>
            </v-chip-group>
          </v-col>

          <!-- Notes -->
          <v-col cols="12" v-if="translation.notes">
            <div class="text-subtitle-2 text-grey">Notes</div>
            <div class="text-body-2">{{ translation.notes }}</div>
          </v-col>
        </v-row>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          :color="translation.isKnown ? 'error' : 'success'"
          variant="flat"
          @click="toggleKnownStatus"
        >
          {{ translation.isKnown ? 'Mark as Unknown' : 'Mark as Known' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { useVocabularyStore } from '@/stores/vocabulary'

const props = defineProps({
  modelValue: Boolean,
  translation: Object
})

const emit = defineEmits(['update:modelValue'])

const vocabularyStore = useVocabularyStore()

const getDifficultyColor = (difficulty) => {
  const colors = {
    EASY: 'green',
    MEDIUM: 'orange',
    HARD: 'red'
  }
  return colors[difficulty] || 'grey'
}

const toggleKnownStatus = async () => {
  if (!props.translation) return
  
  try {
    const newKnownState = !props.translation.isKnown
    await vocabularyStore.toggleWordKnown(props.translation.id, newKnownState)
    props.translation.isKnown = newKnownState
  } catch (error) {
    console.error('Failed to toggle known status:', error)
    alert('Failed to update word status.')
  }
}
</script>
