import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { v4 as uuid } from 'uuid';
import * as pdfjsLib from "pdfjs-dist";

const InstitutionProviderDashboard = () => {
  const navigate = useNavigate();

  const uuidFromUuidV4 = () => {
    const newUuid = uuid();
    return newUuid;
  };

  const [formData, setFormData] = useState({
    institutionName: "",
    location: "",
    type: "",
    Established: "",
    placement_records: "",
    courses: [],
    Affiliation: "",
    hostel_facilities: "",
    admissionFees: "",
    mess_facilities: "",
    websiteLink: "",
    average_package: "",
    highest_package: "",
    reap_percentile_required: "",
  });
  const [courses, setCourses] = useState([]);
  const [courseInput, setCourseInput] = useState({ name: "", placementStats: "", cutoff: "" });
  const [institutionDataList, setInstitutionDataList] = useState([]);
  const [rejectedDataList, setRejectedDataList] = useState([]);
  const [EditStatus, setEditStatus] = useState(undefined);
  const [pdfContent, setPdfContent] = useState("");

  useEffect(() => {
    const storedData = JSON.parse(localStorage.getItem("institutionData")) || [];
    setInstitutionDataList(storedData);

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
      keyId,
      pdfContent,
    };

    const response = { ok: true };

    if (response.ok) {
      const updatedInstitutionData = [...institutionDataList, data];
      localStorage.setItem("institutionData", JSON.stringify(updatedInstitutionData));
      setInstitutionDataList(updatedInstitutionData);

      alert("Data Submitted Successfully!");
      resetForm();
    }
  };

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
    setPdfContent("");
  };

  const extractTextFromPDF = async (file) => {
    try {
      const fileReader = new FileReader();
      fileReader.onload = async () => {
        const typedArray = new Uint8Array(fileReader.result);

        const pdf = await pdfjsLib.getDocument(typedArray).promise;
        let text = "";

        for (let i = 1; i <= pdf.numPages; i++) {
          const page = await pdf.getPage(i);
          const textContent = await page.getTextContent();
          const pageText = textContent.items.map((item) => item.str).join(" ");
          text += pageText + "\n";
        }

        setPdfContent(text);
        alert("PDF content extracted successfully!");
      };

      fileReader.readAsArrayBuffer(file);
    } catch (error) {
      console.error("Error extracting text from PDF:", error);
      alert("Failed to extract text from PDF");
    }
  };

  const handlePDFUpload = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/pdf") {
      extractTextFromPDF(file);
    } else {
      alert("Please upload a valid PDF file.");
    }
  };

  const logout = () => {
    navigate('/');
  };

  return (
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
        <input
          type="file"
          accept="application/pdf"
          onChange={handlePDFUpload}
          className="border p-2 rounded mb-4 w-full"
        />
        {pdfContent && (
          <textarea
            rows={10}
            className="border p-2 rounded w-full mb-4"
            value={pdfContent}
            readOnly
          ></textarea>
        )}
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
                {course.name} | Placements: {course.placementStats} | Cutoff: {course.cutoff}
              </li>
            ))}
          </ul>
        )}
        <button
          onClick={handleSubmit}
          className="bg-green-500 text-white px-4 py-2 rounded mt-4"
        >
          Submit
        </button>
      </div>

      <button
        onClick={logout}
        className="bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-800 m-2"
      >
        Logout
      </button>
    </div>
  );
};

export default InstitutionProviderDashboard;
