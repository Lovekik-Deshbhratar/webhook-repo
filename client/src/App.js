import "./App.css";
import { useEffect, useState } from "react";
import axios from "axios";
function App() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://localhost:5000/webhook/get_all"
        );
        setEvents(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, []);
  console.log(events);
  return (
    <div className="h-[100vh] font-mono">
      <div className="h-full flex justify-center">
        <div className="space-y-3 text-lg p-4">
          <h1 className="text-center font-bold text-red-600 mb-5">
            WebHook from repo action-repo
          </h1>
          {events.map((event) => (
            <h1 key={event.request_id}>
              {event.action === "PUSH" ? (
                <>
                  <span className="font-semibold">{event.author}</span> pushed
                  to <span className="font-semibold">{event.to_branch}</span> on{" "}
                  <span className="font-semibold">
                    {new Date(event.timestamp).toLocaleString()}
                  </span>
                </>
              ) : event.action === "PULL_REQUEST_opened" ? (
                <>
                  <span className="font-semibold">{event.author}</span>{" "}
                  submitted a pull request from{" "}
                  <span className="font-semibold">{event.from_branch}</span> to{" "}
                  <span className="font-semibold">{event.to_branch}</span> on{" "}
                  <span className="font-semibold">
                    {new Date(event.timestamp).toLocaleString()}
                  </span>
                </>
              ) : event.action === "PULL_REQUEST_merged" ? (
                <>
                  <span className="font-semibold">{event.author}</span> merged
                  branch from{" "}
                  <span className="font-semibold">{event.from_branch}</span> to{" "}
                  <span className="font-semibold">{event.to_branch}</span> on{" "}
                  <span className="font-semibold">
                    {new Date(event.timestamp).toLocaleString()}
                  </span>
                </>
              ) : null}
            </h1>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
