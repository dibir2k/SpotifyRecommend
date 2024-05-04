import React from "react";
// import { Table } from 'react-bootstrap';
// import CustomPagination from './CustomPagination';
// import { useState, useEffect } from "react";
import ListOfTracks from "../utils";

const TracksPage = () => {
    const trackData = JSON.parse(localStorage.getItem("trackData") || null);

    return (
        <div>
            <ListOfTracks tracks={trackData} />
        </div>
    );
//     console.log(typeof trackData);
//     const [searchFilter, setSearchFilter] = useState(''); // filter the search
//     const [currentPage, setCurrentPage] = useState(1);
//     const pageSize = 25;
//     useEffect(() => {
//         setCurrentPage(1);
//     }, [searchFilter]);
    
//     const handleFilter = (e) => {
//         setSearchFilter(e.target.value);
//     };
    
//     const filteredData = trackData.filter(
//         (item) =>
//           item.artist_name.toLowerCase().includes(searchFilter.toLowerCase()) ||
//           item.track_name.toString().includes(searchFilter)
//     );
    
//     const paginatedData = filteredData.slice(
//         (currentPage - 1) * pageSize,
//         currentPage * pageSize
//     );

//     return (
//     <div className='fluid container'>
//       <div className='mb-2 fw-50'>Tracks</div>
//       <input
//         style={{ width: "200px" }}
//         className='form-control mb-2'
//         placeholder='Search'
//         value={searchFilter}
//         onChange={handleFilter}
//       />
//       <Table striped bordered hover id='table'>
//         <tbody>
//           <tr>
//             <th style={{ width: '4%' }}>#</th>
//             <th>Track Name</th>
//             <th>Artist Name</th>
//           </tr>
//           {paginatedData.length > 0 ? (
//             paginatedData.map((item, i) => (
//               <tr key={i} style={{ background: '#fff' }}>
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
//       </Table>
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
}

export default TracksPage