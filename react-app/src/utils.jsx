// import React from "react";
// import { Table } from 'react-bootstrap';
// import CustomPagination from './components/CustomPagination';
// import { useState, useEffect } from "react";

// export default function ListOfTracks({tracks}) {
//     console.log(typeof tracks);
//     const [searchFilter, setSearchFilter] = useState(''); // filter the search
//     const [currentPage, setCurrentPage] = useState(1);
//     const pageSize = 25;
//     useEffect(() => {
//         setCurrentPage(1);
//     }, [searchFilter]);
    
//     const handleFilter = (e) => {
//         setSearchFilter(e.target.value);
//     };
    
//     const filteredData = tracks.filter(
//         (item) =>
//           item.artist_name.toLowerCase().includes(searchFilter.toLowerCase()) ||
//           item.track_name.toString().includes(searchFilter)
//     );

//     const handleRowClick = (id) => {
//         let url = "http://open.spotify.com/track/"
//         if (id.includes("track:")) url = url + id.split("track:")[1];
//         else url = "http://open.spotify.com/track/" + id;
//         console.log(url)
//         window.open(url, '_blank'); // Open the URI in a new tab
//       };
    
//     const paginatedData = filteredData.slice(
//         (currentPage - 1) * pageSize,
//         currentPage * pageSize
//     );

//     return (
//     <div className='custom-container'>
//       <div className='mb-2 fw-50'></div>
//       <input
//         style={{ width: "200px" }}
//         className='form-control mb-2'
//         placeholder='Search'
//         value={searchFilter}
//         onChange={handleFilter}
//       />
//       <table id='table'>
//         <tbody>
//           <tr>
//             <th style={{ width: '4%' }}></th>
//             <th>Track Name</th>
//             <th>Artist Name</th>
//           </tr>
//           {paginatedData.length > 0 ? (
//             paginatedData.map((item, i) => (
//               <tr key={i} onClick={() => handleRowClick(item.track_id)} style={{ cursor: 'pointer' }}>
//                 <td>{(currentPage - 1) * pageSize + i + 1}</td>
//                 <td>{item.track_name}</td>
//                 <td>{item.artist_name}</td>
//               </tr>
//             ))
//           ) : (
//             <tr>
//               <td colSpan="3">No data found</td>
//             </tr>
//           )}
//         </tbody>
//       </table>
//       {filteredData.length > 0 &&
//         <>
//           <CustomPagination
//             itemsCount={filteredData.length}
//             itemsPerPage={pageSize}
//             currentPage={currentPage}
//             setCurrentPage={setCurrentPage}
//             alwaysShown={true}
//           />
//         </>
//       }
//     </div>
//   );
// };


import React from "react";
import { Table } from 'react-bootstrap';
import CustomPagination from './components/CustomPagination';
import { useState, useEffect, Fragment } from "react";
import { RotatingLines } from "react-loader-spinner";

export function ListOfTracks({tracks}) {
    console.log(typeof tracks);
    const [searchFilter, setSearchFilter] = useState(''); // filter the search
    const [currentPage, setCurrentPage] = useState(1);
    const pageSize = 25;
    useEffect(() => {
        setCurrentPage(1);
    }, [searchFilter]);
    
    const handleFilter = (e) => {
        setSearchFilter(e.target.value);
    };
    
    const filteredData = tracks.filter(
        (item) =>
          item.artist_name.toLowerCase().includes(searchFilter.toLowerCase()) ||
          item.track_name.toString().includes(searchFilter)
    );

    const handleRowClick = (id) => {
        let url = "http://open.spotify.com/track/"
        if (id.includes("track:")) url = url + id.split("track:")[1];
        else url = "http://open.spotify.com/track/" + id;
        console.log(url)
        window.open(url, '_blank'); // Open the URI in a new tab
      };
    
    const paginatedData = filteredData.slice(
        (currentPage - 1) * pageSize,
        currentPage * pageSize
    );

    return (
    <div className='custom-container'>
      <div className='mb-2 fw-50'></div>
      <input
        style={{ width: "200px" }}
        className='form-control mb-2'
        placeholder='Search'
        value={searchFilter}
        onChange={handleFilter}
      />
      <div className="tracks">
            <ul>
            {paginatedData.length > 0 ? (
             paginatedData.map((track, i) => (
                <Fragment key={i}>
                  <div className="track-info" onClick={() => handleRowClick(track.track_id)} style={{ cursor: 'pointer' }}>
                    {track.image ? (
                      <li className="art">
                        <img
                          alt="album art"
                          src={track.image}
                        ></img>
                      </li>
                    ) : (
                      ""
                    )}
                    <li className="name">
                      {track.track_name}
                      </li>
                    <li className="track-details">
                      <span>
                        {track.artist_name}
                      </span>
                      <span className="album">{track.album_name}</span>
                    </li>
                    <li className="duration">
                      <span>{track.duration}</span>
                    </li>
                  </div>
                </Fragment>
             ))
              ) : (
                              <div className="NotFound">
                                <li>No data found</li>
                              </div>
                            )}
            </ul>
          </div>
      {filteredData.length > 0 &&
        <>
          <CustomPagination
            itemsCount={filteredData.length}
            itemsPerPage={pageSize}
            currentPage={currentPage}
            setCurrentPage={setCurrentPage}
            alwaysShown={true}
          />
        </>
      }
    </div>
  );
};

export function Loader() {
  return (
    <RotatingLines
      strokeColor="grey"
      strokeWidth="5"
      animationDuration="0.75"
      width="96"
      visible={true}
    />
  )
}