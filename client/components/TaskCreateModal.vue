<script setup>
const runtimeConfig = useRuntimeConfig();
const toast = useToast();
const isOpen = defineModel();

const state = ref({
  name: undefined,
});

const handleSubmit = async () => {
  const { status } = await useFetch(runtimeConfig.public.apiUrl + "/tasks", {
    method: "POST",
    body: {
      name: state.value.name,
    },
  });

  let toastData;
  if (status.value == "success")
    toastData = { title: "Task has been added!", color: "primary" };
  else
    toastData = {
      title: "There was an error while adding your task!",
      color: "red",
    };

  toast.add(toastData);

  state.value.name = undefined;
  isOpen.value = false;
};
</script>

<template>
  <UModal v-model="isOpen">
    <UForm :state="state" @submit="handleSubmit" class="p-8 space-y-4">
      <UFormGroup label="Task name">
        <UInput v-model="state.name" />
      </UFormGroup>

      <UButton type="submit" label="Add a task" />
    </UForm>
  </UModal>
</template>
