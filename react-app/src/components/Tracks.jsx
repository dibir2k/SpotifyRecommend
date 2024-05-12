import React from "react";
import { ListOfTracks, Loader } from "../utils";

const TracksPage = () => {
    const trackData = JSON.parse(localStorage.getItem("trackData") || null);

    return (
        <div className="custom-container spacer">
            <ListOfTracks tracks={trackData} />
        </div>
    );
}

export default TracksPage