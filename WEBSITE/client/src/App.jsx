import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom";
import { NewDisp } from "./pages/NewDisp";
import { Register } from "./pages/Register";
import { Login } from "./pages/Login";
import { Inicio } from "./pages/Inicio";
import { UpdateDisp } from "./pages/UpdateDisp";
import { DeleteDisp } from "./pages/DeleteDisp";
import { MistakeDisp } from "./pages/MistakeDisp";
import { ListDisp } from "./pages/ListDisp";
import { RegLocation } from "./pages/RegLocation";

function App() {
  return (
    <BrowserRouter>
      <Routes>  
          <Route path="/" element={<Navigate to="/Ingresar" />}></Route>
          <Route path="/Register" element={<Register />}></Route>
          <Route path="/Ingresar" element={<Login />}></Route>
          <Route path="/Inicio" element={<Inicio />}></Route>
          <Route path="/New" element={<NewDisp />}></Route>
          <Route path="/New/:id" element={<NewDisp />}></Route>
          <Route path="/Update" element={<UpdateDisp />}></Route>
          <Route path="/Delete" element={<DeleteDisp />}></Route>
          <Route path="/Mistake" element={<MistakeDisp />}></Route>
          <Route path="/List" element={<ListDisp />}></Route>
          <Route path="/RegL" element={<RegLocation />}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
