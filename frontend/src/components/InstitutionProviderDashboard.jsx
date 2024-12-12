import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { v4 as uuid } from 'uuid'

const InstitutionProviderDashboard = () => {
  const navigate = useNavigate();

  const uuidFromUuidV4 = () => {
    const newUuid = uuid()
    return (newUuid)
  }

  const [formData, setFormData] = useState({
    institutionName: "",
    location: "",
    type:"",
    Established:"",
    placement_records: "",
    courses:[],
    Affiliation: "",
    hostel_facilities: "",
    admissionFees: "",
    mess_facilities: "",
    websiteLink: "",
    average_package: "",
    highest_package: "",
    reap_percentile_required: ""
  });
  const [courses, setCourses] = useState([]);
  const [courseInput, setCourseInput] = useState({ name: "", placementStats: "", cutoff: "" });

  const [institutionDataList, setInstitutionDataList] = useState([]);
  const [rejectedDataList, setRejectedDataList] = useState([]);
  const [EditStatus, setEditStatus] = useState(undefined);


  useEffect(() => {
    // Load institution data
    const storedData = JSON.parse(localStorage.getItem("institutionData")) || [];
    setInstitutionDataList(storedData);

    // Load rejected data
    const rejectedData = JSON.parse(localStorage.getItem("rejectedData")) || [];
    setRejectedDataList(rejectedData);
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = () => {
    const keyId = uuidFromUuidV4();
    const data = {
      ...formData,
      courses,
      keyId
    };

    // Log data for debug purposes
    console.log("Submitted Data:", data);

    const response = { "ok": true };

    if (response.ok) {
      const updatedInstitutionData = [...institutionDataList, data];
      localStorage.setItem("institutionData", JSON.stringify(updatedInstitutionData));
      setInstitutionDataList(updatedInstitutionData);

      alert("Data Submitted Successfully!");
      resetForm();
    }
  }

  const addCourse = () => {
    setCourses([...courses, courseInput]);
    setCourseInput({ name: "", placementStats: "", cutoff: "" });
  };

  const resetForm = () => {
    setFormData({
      institutionName: "",
      location: "",
      type: "",
      websiteLink: "",
      courses: [],
      Established: "",
      Affiliation: "",
      hostel_facilities: "",
      admissionFees: "",
      mess_facilities: "",
      reap_percentile_required: "",
      placement_records: "",
      average_package: "",
      highest_package: "",
    });
    setCourses([]);
  };

  const logout = () => {
    navigate('/');               // Redirect to the login page
  };


  const handleEdit = (data) => {
    setEditStatus("Edit the form and submit again!");
    setFormData(data);
    setCourses(data.courses || []);
  };

  const handleResubmit = async (record) => {
    const data = {
      ...formData,
      courses,
      keyId: record.keyId
    };

    // Retrieve existing data from localStorage (institution data)
    let storedData = await JSON.parse(localStorage.getItem("institutionData")) || [];
    if(storedData.length === 0){
      storedData=[data]
    }
    // Find the index of the record to update based on keyId
    let index = -1;
    for (let i = 0; i < storedData.length; i++) {
      if (storedData[i].keyId === data.keyId) {
        index = i;
        break;
      }
    }

    if (index !== -1) {
      // Remove the old record by its keyId and add the new updated record
      storedData.splice(index, 1, data);

    }
    // Save the updated list back to localStorage
    localStorage.setItem("institutionData", JSON.stringify(storedData));

    // Optionally update the state with the new data
    setInstitutionDataList(storedData);

    // Remove rejected data after resubmission
    const updatedRejectedData = rejectedDataList.filter((item) => item.keyId!==data.keyId);
   
    console.log(updatedRejectedData);
    localStorage.setItem("rejectedData", JSON.stringify(updatedRejectedData));
    setRejectedDataList(updatedRejectedData);

    alert("Data Resubmitted!");
    setEditStatus(undefined);
    resetForm();
  };

  return (
    <div>
      <div className="container mx-auto p-6 bg-gray-100 min-h-screen">
        <h1 className="text-2xl font-bold mb-4">Institution Provider Dashboard</h1>

        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl mb-2 font-semibold">Institution Details</h2>
          <input
            type="text"
            placeholder="Institution Name"
            name="institutionName"
            value={formData.institutionName}
            onChange={handleInputChange}
            className="border p-2 rounded mb-4 w-full"
          />
          <input
            type="text"
            placeholder="Location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            className="border p-2 rounded mb-4 w-full"
          />
          <input
            type="text"
            placeholder="Type"
            name="type"
            value={formData.type}
            onChange={handleInputChange}
            className="border p-2 rounded mb-4 w-full"
          />
          <input
            type="text"
            placeholder="Website Link"
            name="websiteLink"
            value={formData.websiteLink}
            onChange={handleInputChange}
            className="border p-2 rounded mb-4 w-full"
          />


          <h2 className="text-xl mb-2 font-semibold">Courses</h2>
          <div className="flex gap-2 mb-4">
            <input
              type="text"
              placeholder="Course Name"
              value={courseInput.name}
              onChange={(e) => setCourseInput({ ...courseInput, name: e.target.value })}
              className="border p-2 rounded flex-grow"
            />
            <input
              type="text"
              placeholder="Placement Stats"
              value={courseInput.placementStats}
              onChange={(e) => setCourseInput({ ...courseInput, placementStats: e.target.value })}
              className="border p-2 rounded flex-grow"
            />
            <input
              type="text"
              placeholder="Cutoff"
              value={courseInput.cutoff}
              onChange={(e) => setCourseInput({ ...courseInput, cutoff: e.target.value })}
              className="border p-2 rounded flex-grow"
            />
            <button onClick={addCourse} className="bg-blue-500 text-white px-4 py-2 rounded">
              Add Course
            </button>
          </div>
          {courses.length > 0 && (
            <ul className="list-disc pl-6">
              {courses.map((course, idx) => (
                <li key={idx}>
                  Courses: {course.name} | Placements: {course.placementStats} | Cutoff: {course.cutoff}
                </li>
              ))}
            </ul>
          )}


          <p className="text-xl mb-2 font-semibold">Established</p>
          <input
            type="text"
            placeholder="Established"
            value={courseInput.Established}
            onChange={handleInputChange}
            className="border p-2 rounded w-full"
          />
          <p className="text-xl mb-2 font-semibold">Affiliation</p>
          <input
            type="text"
            placeholder="Affiliation"
            value={courseInput.Affiliation}
            onChange={handleInputChange}
            className="border p-2 rounded w-full"
          />
          <p className="text-xl mb-2 font-semibold">Hostel Facilities</p>
          <input
            type="text"
            placeholder="Hostel Facilities(Put 0 if not)"
            value={courseInput.hostel_facilities}
            onChange={handleInputChange}
            className="border p-2 rounded w-full"
          />
          <p className="text-xl mb-2 font-semibold">Mess Facilities</p>
          <input
            type="text"
            placeholder="Mess Facilities(Put 0 if not)"
            value={courseInput.mess_facilities}
            onChange={handleInputChange}
            className="border p-2 rounded w-full"
          />
          <p className="text-xl mb-2 font-semibold">Precentile Required</p>
          <input
            type="text"
            placeholder="Precentile Required"
            value={courseInput.reap_percentile_required}
            onChange={handleInputChange}
            className="border p-2 rounded w-full"
          />

          <p className="text-xl mb-2 font-semibold">Admission Fees</p>
          <input
            type="number"
            placeholder="Admission Fees"
            name="admissionFees"
            value={formData.admissionFees}
            onChange={handleInputChange}
            className="border p-2 rounded mb-4 w-full"
          />
          <p className="text-xl mb-2 font-semibold">Average Package</p>
          <input
            type="number"
            placeholder="Average Package"
            name="average_package"
            value={formData.average_package}
            onChange={handleInputChange}
            className="border p-2 rounded mb-4 w-full"
          />
          <p className="text-xl mb-2 font-semibold">Highest Package</p>
          <input
            type="number"
            placeholder="Highest Package"
            name="highest_package"
            value={formData.highest_package}
            onChange={handleInputChange}
            className="border p-2 rounded mb-4 w-full"
          />
          <p className="text-xl mb-2 font-semibold">Placement Records</p>
          <input
            type="number"
            placeholder="Placement Records"
            name="placement_records"
            value={formData.placement_records}
            onChange={handleInputChange}
            className="border p-2 rounded mb-4 w-full"
          />

          {
            !EditStatus &&
            <button onClick={handleSubmit} className="bg-green-500 text-white px-4 py-2 rounded mt-4">
              Submit
            </button>
          }
        </div>


        {/* Display Rejected Data */}
        <div className="mb-6">
          <h2 className="text-lg font-semibold mb-4 text-gray-800">Rejected Data</h2>
          {rejectedDataList && rejectedDataList.length > 0 ? (
            rejectedDataList.map((data, index) => (
              <div
                key={index}
                className="p-4 border rounded-lg mb-4 bg-red-100 hover:shadow-md transition duration-300"
              >
                <ul className="text-black font-medium mb-2">
                  <p className="font-bold">Key: {data.keyId}</p>
                  <p className="font-bold">Institution: {data.institutionName}</p>
                  <p className="font-bold">Rejection Reason: {data.rejectionComment}</p>
                </ul>
                <p className="font-bold italic mb-2">{EditStatus}</p>
                <div className="flex gap-4">
                  <button
                    className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700 transition duration-300"
                    onClick={() => handleEdit(data)}
                  >
                    Edit
                  </button>


                  <button
                    className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-700 transition duration-300"
                    onClick={() => handleResubmit(data)}
                  >
                    Resubmit
                  </button>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No rejected data available.</p>
          )}
        </div>

        {/* Display Submitted Data */}
        <div>
          <h2 className="text-lg font-semibold mb-4 text-gray-800">Submitted Data</h2>
          {institutionDataList && institutionDataList.length > 0 ? (
            institutionDataList.map((data, index) => (
              <div
                key={index}
                className="p-4 border rounded-lg mb-4 bg-green-100 hover:shadow-md transition duration-300"
              >
                <ul className="text-black font-medium mb-2">
                  <li className="font-bold">Key:{data.keyId}</li>
                  <li className="font-bold">Institution:{data.institutionName}</li>
                  <li className="font-bold">Institution:{data.location}</li>
                </ul>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No submitted data available.</p>
          )}
        </div>
        <button
          onClick={logout}
          className="bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-800 m-2"
        >
          Logout
        </button>
      </div>
    </div>


  );
};

export default InstitutionProviderDashboard;
