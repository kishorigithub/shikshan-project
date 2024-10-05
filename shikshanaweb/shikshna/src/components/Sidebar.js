import React, { useEffect, useState } from 'react';

const Sidebar = () => {

  
  const [activeTab, setActiveTab] = useState('Syllabus'); // Default to 'Syllabus'

  // Function to render content based on the active tab
  const renderContent = () => {
    switch (activeTab) {
      case 'Syllabus':
        return <div>This is the Syllabus content.</div>;
      case 'Timetable':
        return <div>This is the Timetable content.</div>;
      case 'Assignments':
        return <div>This is the Assignments content.</div>;
      case 'E-learning':
        return <div>This is the E-learning content.</div>;
      case 'Games':
        return <div>This is the Games content.</div>;
      case 'Chats':
        return <div>This is the Chats content.</div>;
      case 'Reportcard':
        return <div>This is the Report Card content.</div>;
      case 'Logout':
        return <div>Logout content (or handle logout here).</div>;
      default:
        return <div>Select a tab to see content.</div>;
    }
  };

  return (
    <div style={{ display: 'flex' }}>
      {/* Sidebar Section */}
      <div className="sidebar">
        <ul>
          <li onClick={() => setActiveTab('Syllabus')}>Syllabus</li>
          <li onClick={() => setActiveTab('Timetable')}>Timetable</li>
          <li onClick={() => setActiveTab('Assignments')}>Assignments</li>
          <li onClick={() => setActiveTab('E-learning')}>E-learning</li>
          <li onClick={() => setActiveTab('Games')}>Games</li>
          <li onClick={() => setActiveTab('Chats')}>Chats</li>
          <li onClick={() => setActiveTab('Reportcard')}>Reportcard</li>
          <li onClick={() => setActiveTab('Logout')}>Logout</li>
        </ul>
      </div>

      {/* Main Content Section */}
      <div className="main-content" style={{ marginLeft: '20px', padding: '20px' }}>
        {renderContent()}
      </div>
    </div>
  );
};

export default Sidebar;
