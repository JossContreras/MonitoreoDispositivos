import { useEffect, useState } from "react"
import { GetAllList } from "../api/List.api";
import style from "../styles/ListDispG.module.css"
import { useNavigate } from "react-router-dom";

export function ListDispG () {

    const navigate = useNavigate()

    const [list, setList] = useState([]);

    useEffect (() => {
        async function loadList () {
            const res = await GetAllList()
            setList(res.data);
        }
        loadList();
    }, [])

    return (
        <div className={style.containerL}>
            <h1 className={style.titleL}>Lista de elementos</h1>
            <div className={style.divider}></div>
            <div className={style.container}>
            {list.map(list => (
                <div className={style.row} key={list.id_inventario}>
                    <div className={style.field}>
                        <label>Tipo Dispostivo</label>
                        <input type="text" value={list.tipo_elemento} readOnly/>
                    </div>

                    <div className={style.field}>
                        <label>ID inventario</label>
                        <input type="text" value={list.id_inventario} readOnly/>
                    </div>

                    <div className={style.field}>
                        <label>Marca</label>
                        <input type="text" value={list.nombre} readOnly/>
                    </div>

                    {/*<div className={style.field}>
                        <label>Estado</label>
                        <input type="text" value={list.estado} readOnly/>
                    </div>*/}
                    
                    <div className={style.field}>
                        <label>Fecha</label>
                        <input type="text" value={list.fecha_adquisicion} readOnly/>
                    </div>

                    <div className={style.field}>
                        <label>ID ubicacion</label>
                        <input type="text" value={list.id_ubicacion} readOnly/>
                    </div>

                    <div onClick={() => {
                            navigate(`/New/${list.id_inventario}`)
                        }} className={style.buttons}>
                        <button className={style.edit}>Editar</button>
                    
                        <button onClick={() => {
                            navigate(`/New/${list.id_inventario}`)
                        }}
                         className={style.delete}>Eliminar</button>
                    </div>
                </div>
            ))}
            </div>
        </div>
    )
}