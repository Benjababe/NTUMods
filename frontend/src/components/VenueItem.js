const VenueItem = ({ venue, loadTimeslots }) => {
    return (
        <div>
            <button
                className="btn-venue"
                onClick={() => loadTimeslots(venue.id)}>
                {venue.name}
            </button>
        </div>
    );
}

export default VenueItem;