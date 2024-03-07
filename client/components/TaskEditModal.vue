<script setup>
const runtimeConfig = useRuntimeConfig();
const toast = useToast();
const isOpen = defineModel();

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
});

const state = ref({
  name: props.task.name,
  is_done: props.task.is_done,
});

const handleSubmit = async () => {
  const { status } = await useFetch(
    runtimeConfig.public.apiUrl + "/tasks/" + props.task.id,
    {
      method: "PUT",
      body: {
        name: state.value.name,
        is_done: state.value.is_done,
      },
    },
  );

  let toastData;
  if (status.value == "success")
    toastData = { title: "Task has been edited!", color: "blue" };
  else
    toastData = {
      title: "There was an error while editing your task!",
      color: "red",
    };

  toast.add(toastData);

  state.value.name = undefined;
  state.value.is_done = undefined;
  isOpen.value = false;
};
</script>

<template>
  <UModal v-model="isOpen">
    <UCard>
      <template #header>
        <h2 class="text-xl font-semibold">{{ state.name }}</h2>
      </template>

      <UForm :state="state" @submit="handleSubmit" class="space-y-4">
        <UFormGroup label="ID">
          <UInput :placeholder="props.task.id" disabled />
        </UFormGroup>

        <UFormGroup label="Name">
          <UInput v-model="state.name" />
        </UFormGroup>

        <UFormGroup label="Done">
          <UCheckbox v-model="state.is_done" />
        </UFormGroup>

        <UButton type="submit" label="Edit" />
      </UForm>
    </UCard>
  </UModal>
</template>
