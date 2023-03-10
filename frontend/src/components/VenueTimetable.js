import Timetable from 'react-timetable-events';

const VenueTimetable = ({ timeslots }) => {
    const dayMap = {
        "MON": "monday",
        "TUE": "tuesday",
        "WED": "wednesday",
        "THU": "thursday",
        "FRI": "friday"
    };

    let events = {
        monday: [],
        tuesday: [],
        wednesday: [],
        thursday: [],
        friday: []
    };

    timeslots.forEach((timeslot) => {
        const day = dayMap[timeslot["day"]];

        // ignore weekend timeslots
        if (day !== undefined) {
            events[day].push({
                id: timeslot.id,
                name: `${timeslot.module_code} ${timeslot.type} ${timeslot.group} ${timeslot.index}`,
                startTime: new Date("1970-01-01T" + timeslot.time_start),
                endTime: new Date("1970-01-01T" + timeslot.time_end)
            });
        }
    });

    return (<Timetable
        events={events}
        style={{ minHeight: "48rem", minWidth: "36rem", fontSize: "smaller" }}
    />);
}

export default VenueTimetable;