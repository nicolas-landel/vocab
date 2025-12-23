<template>
  <VDialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="600">
    <VCard v-if="translation">
      <VCardTitle class="d-flex justify-space-between align-center">
        <span>{{ translation.text }}</span>
        <VBtn icon="mdi-close" variant="text" @click="$emit('update:modelValue', false)"></VBtn>
      </VCardTitle>

      <VDivider></VDivider>

      <VCardText class="pt-4">
        <VRow>
          <!-- Native Language Translation -->
          <VCol cols="12">
            <div class="text-subtitle-2 text-grey">{{ t('wordDetail.translation') }}</div>
            <div class="text-h6">{{ translation.masterWord?.text || '-' }}</div>
          </VCol>

          <!-- Gender -->
          <VCol cols="6" v-if="translation.gender">
            <div class="text-subtitle-2 text-grey">{{ t('wordDetail.gender') }}</div>
            <div class="text-body-1">{{ translation.gender }}</div>
          </VCol>

          <!-- Plural Form -->
          <VCol cols="6" v-if="translation.plural">
            <div class="text-subtitle-2 text-grey">{{ t('wordDetail.plural') }}</div>
            <div class="text-body-1">{{ translation.plural }}</div>
          </VCol>

          <!-- Domain -->
          <VCol cols="6">
            <div class="text-subtitle-2 text-grey">{{ t('wordDetail.domain') }}</div>
            <div class="text-body-1">{{ translation.masterWord?.domain?.code ? t(`domains.${translation.masterWord.domain.code}`) : '-' }}</div>
          </VCol>

          <!-- Difficulty -->
          <VCol cols="6">
            <div class="text-subtitle-2 text-grey">{{ t('wordDetail.difficulty') }}</div>
            <VChip :color="getDifficultyColor(translation.difficulty)" size="small">
              {{ t(`difficulties.${translation.difficulty.toLowerCase()}`) }}
            </VChip>
          </VCol>

          <!-- Example Sentence -->
          <VCol cols="12" v-if="translation.exampleSentence">
            <div class="text-subtitle-2 text-grey">{{ t('wordDetail.example') }}</div>
            <div class="text-body-1 font-italic">"{{ translation.exampleSentence }}"</div>
          </VCol>

          <!-- Pronunciation -->
          <VCol cols="12" v-if="translation.pronunciation">
            <div class="text-subtitle-2 text-grey">{{ t('wordDetail.pronunciation') }}</div>
            <div class="text-body-1">{{ translation.pronunciation }}</div>
          </VCol>

          <!-- Audio Pronunciation -->
          <VCol cols="12" v-if="translation.audioUrl">
            <div class="text-subtitle-2 text-grey mb-2">{{ t('wordDetail.listen') }}</div>
            <audio controls :src="translation.audioUrl" class="w-100"></audio>
          </VCol>

          <!-- Synonyms -->
          <VCol cols="12" v-if="translation.synonyms && translation.synonyms.length > 0">
            <div class="text-subtitle-2 text-grey mb-2">{{ t('wordDetail.synonyms') }}</div>
            <VChipGroup>
              <VChip
                v-for="(synonym, index) in translation.synonyms"
                :key="index"
                size="small"
                variant="outlined"
              >
                {{ synonym }}
              </VChip>
            </VChipGroup>
          </VCol>

          <!-- Notes -->
          <VCol cols="12" v-if="translation.notes">
            <div class="text-subtitle-2 text-grey">{{ t('wordDetail.notes') }}</div>
            <div class="text-body-2">{{ translation.notes }}</div>
          </VCol>
        </VRow>
      </VCardText>

      <VDivider></VDivider>

      <VCardActions>
        <VSpacer></VSpacer>
        <VBtn
          :color="translation.isKnown ? 'error' : 'success'"
          variant="flat"
          @click="toggleKnownStatus"
        >
          {{ translation.isKnown ? t('wordDetail.markAsUnknown') : t('wordDetail.markAsKnown') }}
        </VBtn>
      </VCardActions>
    </VCard>
  </VDialog>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useVocabularyStore } from '@/stores/vocabulary'

const { t } = useI18n()

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
    console.error(t('vocabulary.failedToToggle'), error)
    alert(t('vocabulary.failedToToggle'))
  }
}
</script>
