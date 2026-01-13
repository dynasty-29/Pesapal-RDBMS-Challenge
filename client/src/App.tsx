import { useState } from 'react'
import PatientList from './components/PatientList'
import DoctorList from './components/DoctorList'
import AppointmentList from './components/AppointmentList'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('patients')

  return (
    <div className="app">
      <header className="app-header">
        <h1>JDEV26 Healthcare Management System</h1>
        <p>A trivial web app to demonstrate CRUD to the DB</p>
      </header>

      <nav className="app-nav">
        <button 
          className={activeTab === 'patients' ? 'active' : ''}
          onClick={() => setActiveTab('patients')}
        >
          Patients
        </button>
        <button 
          className={activeTab === 'doctors' ? 'active' : ''}
          onClick={() => setActiveTab('doctors')}
        >
          Doctors
        </button>
        <button 
          className={activeTab === 'appointments' ? 'active' : ''}
          onClick={() => setActiveTab('appointments')}
        >
          Appointments
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'patients' && <PatientList />}
        {activeTab === 'doctors' && <DoctorList />}
        {activeTab === 'appointments' && <AppointmentList />}
      </main>
    </div>
  )
}

export default App