import { Link } from "react-router-dom";
import styles from "../styles/Inicio.module.css";
import { NavBar} from "../components/NavBar.jsx";
import IconoNew from "../assets/img/IconoNew.png";
import IconoDelete from "../assets/img/IconoDelete.png";
import IconoMistakes from "../assets/img/IconoMistakes.png";
import IconoUpdate from "../assets/img/IconoUpdate.png";
import IconoList from "../assets/img/IconoList.png";

export function Inicio () {
    return ( <><NavBar />
        <div>
        <div className={styles.containeri}>
                <h1 className={styles.titlei}>Actividad</h1>
                <div className={styles.divider}></div>
                <div className={styles.tareas}>
                    <Link to="/New" className={styles.tarea}>
                        <img src={IconoNew} alt="Nuevo dispositivo"/>
                        <h2>Nuevo</h2>
                        <p className={styles.green}>Agregue un nuevo dispositivo</p>
                    </Link>

                    <Link to="/Update" className={styles.tarea}>
                        <img src={IconoUpdate} alt="Actuzalizar dispositivo"/>
                        <h2>Actualizar</h2>
                        <p className={styles.green}>Actualice algun dispositivo ya existente</p>
                    </Link>

                    <Link to="/Delete" className={styles.tarea}>
                        <img src={IconoDelete} alt="Eliminar dispositivo"/>
                        <h2>Eliminar</h2>
                        <p className={styles.green}>Elimine algun dispositivo ya existente</p>
                    </Link>

                    <Link to="/Mistake" className={styles.tarea}>
                        <img src={IconoMistakes} alt="Incidentes dispositivos"/>
                        <h2>Inicidentes</h2>
                        <p className={styles.green}>Registre incidentes de los diversos dispositivos</p>
                    </Link>

                    <Link to="/List" className={styles.tarea}>
                        <img src={IconoList} alt="Lista de dispositivos"/>
                        <h2>Lista</h2>
                        <p className={styles.green}>Consulte la lista completa de elementos</p>
                    </Link>
                </div>
            </div>
        </div></>
    )
}