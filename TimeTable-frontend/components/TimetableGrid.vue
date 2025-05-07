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
          <option v-for="s in timeSlots" :key="s.id" :value="s.id">
            {{ s.start }} - {{ s.end }}
          </option>
        </select>
        <select class="py-2 px-1" v-model="form.group">
          <option v-for="g in groups" :key="g.id">{{ g.name }}</option>
        </select>
        <select class="py-2 px-1" v-model="form.teachers">
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

    <h2 class="text-xl font-bold text-gray-700 mb-4">Orar</h2>
    <div class="grid grid-cols-6 gap-px text-gray-800 border border-blue-300">
      <div class="bg-blue-100 font-bold text-gray-700 p-2">Ora</div>
      <div
        v-for="day in days"
        :key="day"
        class="bg-blue-100 text-gray-700 font-bold p-2"
      >
        {{ day }}
      </div>

      <div v-for="slot in timeSlots" :key="slot.id" class="contents">
        <div class="bg-blue-100 p-2 text-sm">
          {{ slot.start }} - {{ slot.end }}
        </div>

        <div
          v-for="day in days"
          :key="day"
          class="border border-blue-300 p-2 min-h-[5rem] bg-white"
        >
          <div
            v-for="s in filteredTimetable.filter(
              (s) => s.day === day && s.slotId === slot.id
            )"
            :key="s.group + s.discipline + s.professor + s.room"
            class="text-sm mb-2 p-1 text-gray-700 rounded bg-blue-100 relative"
          >
            <button
              class="absolute top-1 right-1 text-gray-600 hover:text-red-800 text-xs"
              @click="removeSession(s)"
            >
              x
            </button>
            <strong>{{ s.discipline }}</strong> ({{ s.type }})<br />
            {{ s.group }}<br />
            {{ s.professor }}<br />
            <em>{{ s.room }}</em>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
const timeSlots = [
  { id: 1, start: "08:00", end: "10:00" },
  { id: 2, start: "10:00", end: "12:00" },
  { id: 3, start: "12:00", end: "14:00" },
  { id: 4, start: "14:00", end: "16:00" },
  { id: 5, start: "16:00", end: "18:00" },
];

const activityTypes = ["course", "seminar", "laboratory"];

const timetableStore = useTimetableStore();
const disciplinesStore = useDisciplinesStore();
const groupsStore = useGroupsStore();
const teachersStore = useTeachersStore();
const roomsStore = useRoomsStore();
const classSessionsStore = useClassSessionsStore();

const { timetable } = storeToRefs(timetableStore);
const { classSessions } = storeToRefs(classSessionsStore);
const { disciplines } = storeToRefs(disciplinesStore);
const { teachers } = storeToRefs(teachersStore);
const { groups } = storeToRefs(groupsStore);
const { rooms } = storeToRefs(roomsStore);

onMounted(async () => {
  await disciplinesStore.fetchDisciplines(),
  await groupsStore.fetchGroups(),
  await teachersStore.fetchTeachers(),
  await roomsStore.fetchRooms(),
  // await timetableStore.fetchTimetable();
  await classSessionsStore.fetchClassSessions();
});

const form = reactive({
  day: days[0],
  slotId: timeSlots[0].id,
  group: groups.value[0]?.name || "",
  professor: teachers.value[0]?.name || "", 
  discipline: disciplines.value[0]?.name || "", 
  room: rooms.value[0]?.name || "",
  type: activityTypes[0],
});

const filteredTimetable = computed(() => {
  if (!Array.isArray(classSessions.value)) {
    return [];
  }
  return classSessions.value.filter((s) => {
    return (
      (form.day ? s.day === form.day : true) &&
      (form.slotId ? s.slotId === form.slotId : true) &&
      (form.group ? s.group === form.group : true) &&
      (form.professor ? s.professor === form.professor : true) &&
      (form.discipline ? s.discipline === form.discipline : true) &&
      (form.room ? s.room === form.room : true) &&
      (form.type ? s.type === form.type : true)
    );
  });
});

const addSession = async () => {
  const sessionData = {
    discipline_id: disciplines.value.find(d => d.name === form.discipline)?.id,
    teacher_id: teachers.value.find(t => t.name === form.professor)?.id ?? 1,
    room_id: rooms.value.find(r => r.name === form.room)?.id ?? 1,
    time_slot_id: form.slotId || 1,
    class_type: form.type,
  };
console.log(sessionData);
  await classSessionsStore.addClassSession(sessionData);
};

const removeSession = (sessionToRemove: any) => {
  classSessions.value = classSessions.value.filter(
    (s) => s !== sessionToRemove
  );
};
</script>
