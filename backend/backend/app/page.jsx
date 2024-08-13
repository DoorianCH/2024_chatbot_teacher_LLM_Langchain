"use client"
import { useEffect, useState } from 'react'
import { FaRobot } from "react-icons/fa";
import { PiFinnTheHumanFill } from "react-icons/pi";

export default function Home() {
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState("");
    const[messageList,setMessageList]=useState([]);
    const[questionList,setQuestionList]=useState([]);

    useEffect(() => {
        fetch('http://localhost:5000/')
            .then((response) => response.json())
            .then(data => {
                setMessage(data.message);
                setLoading(false);
            })
    }, [])

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({"message":formData})
            });
            const data = await response.json();
            setMessage(data.message);
            setMessageList([...messageList, data.message]); 
            setQuestionList([...questionList,formData]);
            setFormData('');
        } catch (error) {
        }
    }

    const handleInputChange = (e) => {
        setFormData( e.target.value );
    }

    return (
        <div className='flex flex-col  items-center w-100% h-100%'>
            <div className='flex items-center '>
            <h1 className="text-3xl">{!loading ? "AI에게 물어보세요" : "Loading.."}</h1>
            </div>
            <div className='w-[800px] h-[1000px] border-4  border-purple-900 border flex justify-end flex-col
             rounded-lg '>
            {
                questionList.map((question, index) => (
                    <div key={index} className="text-l font-bold m-3">
                        <div className='flex  w-full justify-end  items-center rounded-lg'>
                            <p className='flex justify-end items-center w-full h-28 border-red-400 border-4 '>
                                <div className='mr-3'>
                                    <PiFinnTheHumanFill size='40'/>
                                    </div>
                                    <div className="mr-3">{question}</div>
                            </p>
                        </div>
                        <div className='flex w-full  ' >
                            <p className='flex  items-center w-full border-yellow-400 h-28 mb-4 mt-4 border-4  rounded-lg'>
                                <div className='mr-3 ml-3'>
                                    <FaRobot size="40"/></div>{messageList[index]}
                            </p>
                        </div>     
                    </div>
                ))
            }
            </div>
            
            <form onSubmit={handleSubmit}>
                <label>
                    Message:
                    <input
                        type="text"
                        placeholder="Chat에 질문해주세요"
                        className="input input-bordered input-primary w-[500px] h-[70px]" name="message" value={formData} onChange={handleInputChange} />
                </label>
                <button type="submit" className="btn w-[100px] h-[70px] m-5">Button</button>
            </form>
        </div>
    )
}
