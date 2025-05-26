<template>
  <div class="p-4 flex flex-col w-full">
    <h2 class="text-xl font-bold text-gray-700 mb-4">Adaugă sesiune</h2>
    <form
      class="flex flex-col w-full items-center mb-2 justify-center"
      @submit.prevent="addSession"
    >
      <div class="flex flex-wrap gap-6 mb-6">
        <select class="py-2 px-1" v-model="form.day">
          <option v-for="d in days" :key="d">{{ d }}</option>
        </select>
        <select class="py-2 px-1" v-model="form.slotId">
          <option v-for="(s, index) in timeSlots" :key="index" :value="`${s.start} - ${s.end}`">
            {{ s.start }} - {{ s.end }}
          </option>
        </select>
        <select class="py-2 px-1" v-model="form.group">
          <option v-for="g in groups" :key="g.id" :value="g">An: {{ g.year.name }}; Semina: {{ g.semian.name }}; Grupa: {{ g.name }} </option>
        </select>
        <select class="py-2 px-1" v-model="form.professor">
          <option v-for="p in teachers" :key="p.id">{{ p.name }}</option>
        </select>
        <select class="py-2 px-1" v-model="form.discipline">
          <option v-for="d in disciplines" :key="d.id">{{ d.name }}</option>
        </select>
        <select class="py-2 px-1" v-model="form.type">
          <option v-for="t in activityTypes" :key="t">{{ t }}</option>
        </select>
        <select class="py-2 px-1" v-model="form.room">
          <option v-for="r in rooms" :key="r.id">{{ r.name }}</option>
        </select>
      </div>
      <button
        class="flex w-[300px] justify-center items-center bg-blue-300 shadow-md text-white px-4 py-2 text-lg rounded"
        type="submit"
      >
        Adaugă
      </button>
    </form>

    <h2 v-if="years.length > 0" class="text-xl font-bold text-gray-700 mb-4">Selectează Anul</h2>
    <div class="flex space-x-4 mb-6">
      <button
        v-for="year in filteredYears"
        :key="year.id"
        :class="[
          'py-2 px-4 border rounded-md text-lg',
          selectedYear === year.id ? 'bg-blue-500 text-white' : 'bg-transparent text-blue-500 border-blue-500'
        ]"
        @click="selectYear(year.id)"
      >
        {{ year.name }}
      </button>
    </div>

    <div class="grid grid-cols-6 gap-px text-gray-800 border border-blue-300">
      <div class="bg-blue-100 font-bold text-gray-700 p-2">Ora</div>
      <div
        v-for="day in days"
        :key="day"
        class="bg-blue-100 text-gray-700 font-bold p-2"
      >
        {{ day }}
      </div>

      <div v-for="(slot, index) in timeSlots" :key="index" class="contents">
        <div class="bg-blue-100 p-2 text-sm">
          {{ slot.start }} - {{ slot.end }}
        </div>

        <div
          v-for="day in days"
          :key="day"
          class="border border-blue-300 p-2 min-h-[5rem] bg-white"
        >
          <div
            v-for="s in classSessions.filter(
              (s) =>
                s.day === day && s.time_slot === `${slot.start} - ${slot.end}`
            )"
            :key="s.discipline + s.teacher + s.room"
            class="text-sm mb-2 p-1 text-gray-700 rounded bg-blue-100 relative"
          >
            <button
              aria-label="Remove session"
              class="absolute top-1 right-1 text-gray-600 hover:text-red-800 text-xs"
              @click="removeSession(s)"
            >
              x
            </button>
            <strong>{{ s.discipline }}</strong> ({{ s.class_type }})<br />
            {{ s.teacher }}<br />
            <em>{{ s.room }}</em>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
const timeSlots = [
  { start: "08:00", end: "10:00" },
  { start: "10:00", end: "12:00" },
  { start: "12:00", end: "14:00" },
  { start: "14:00", end: "16:00" },
  { start: "16:00", end: "18:00" },
  { start: "18:00", end: "20:00" },
];
const activityTypes = ["course", "laboratory", "seminar", "seminar/laboratory"];

const disciplinesStore = useDisciplinesStore();
const groupsStore = useGroupsStore();
const teachersStore = useTeachersStore();
const roomsStore = useRoomsStore();
const classSessionsStore = useClassSessionsStore();
const timeSlotsStore = useTimeSlotsStore();
const yearsStore = useYearsStore();

const { years } = storeToRefs(yearsStore);
const { classSessions } = storeToRefs(classSessionsStore);
const { disciplines } = storeToRefs(disciplinesStore);
const { teachers } = storeToRefs(teachersStore);
const { groups } = storeToRefs(groupsStore);
const { rooms } = storeToRefs(roomsStore);
const { slots } = storeToRefs(timeSlotsStore);

const selectedYear = ref<number | null>(null);

onMounted(async () => {
  await timeSlotsStore.fetchTimeSlots();
  await yearsStore.fetchYears();
  await disciplinesStore.fetchDisciplines(),
  await groupsStore.fetchGroups(),
  await teachersStore.fetchTeachers(),
  await roomsStore.fetchRooms(),
  await classSessionsStore.fetchClassSessions({});
});

const filteredYears = computed(() => {
  const allYear = { id: 0, name: "All" };
  return years && years.value.length > 0 ? [allYear, ...years.value] : [allYear]; 
});


const form = reactive({
  day: "",
  slotId: "",
  group: null as Group | null,
  professor: "",
  discipline: "",
  room: "",
  type: "",
});

const selectYear = async(yearId: number) => {
  selectedYear.value = yearId;
  if(yearId === 0){
    await classSessionsStore.fetchClassSessions({}); 
    return;
  }
  await classSessionsStore.fetchClassSessions({year_id:yearId}); 
};

const addSession = async () => {
  const sessionData = {
    discipline_id: disciplines.value.find((d) => d.name === form.discipline)
      ?.id,
    teacher_id: teachers.value.find((t) => t.name === form.professor)?.id ?? 1,
    room_id: rooms.value.find((t) => t.name === form.room)?.id ?? 1,
    time_slot_id:
      slots.value.find(
        (s) =>
          s.day === form.day &&
          form.slotId === `${s.start_time} - ${s.end_time}`
      )?.id ?? 1,
    class_type: form.type,
    semian_id: form.group?.semian.id,
    year_id:form.group?.year.id,
    group_id: form.group?.id
  };

  await classSessionsStore.addClassSession(sessionData);
};

const removeSession = (sessionToRemove: any) => {
  classSessionsStore.deleteClassSession(sessionToRemove.id);
};
</script>
