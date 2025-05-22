use hyper::service::{make_service_fn, service_fn};
use hyper::{Body, Request, Response, Server, StatusCode};
use std::convert::Infallible;
use std::net::SocketAddr;
use pyo3::prelude::*;
use tokio::runtime::Runtime; // For creating a Tokio runtime

// --- Existing HTTP server code (handle_request, run_server) ---
async fn handle_request(_req: Request<Body>) -> Result<Response<Body>, Infallible> {
    // For now, this is a placeholder. It will eventually call Python handlers.
    Ok(Response::builder()
        .status(StatusCode::OK)
        .body(Body::from("Hello from Rust HTTP Server!"))
        .unwrap())
}

async fn run_rust_server_internal(addr: SocketAddr) { // Renamed to avoid conflict, and made it internal
    let make_svc = make_service_fn(|_conn| async {
        Ok::<_, Infallible>(service_fn(handle_request))
    });

    let server = Server::bind(&addr).serve(make_svc);
    println!("Rust HTTP server listening on http://{}", addr);

    if let Err(e) = server.await {
        eprintln!("server error: {}", e);
    }
}
// --- End of existing HTTP server code ---

// --- PyO3 Exposed Functions ---
#[pyfunction]
fn rust_hello() -> PyResult<String> {
    Ok("Hello from Rust via PyO3!".to_string())
}

#[pyfunction]
fn start_server(py: Python, host: String, port: u16) -> PyResult<()> {
    // Create a new Tokio runtime or get a handle to an existing one if shared.
    // For simplicity, a new runtime is created here.
    // PyO3 recommends using pyo3_asyncio for better integration if your Rust futures
    // need to interact heavily with Python's asyncio loop (e.g. awaiting Python async functions from Rust).
    // For now, we are just spawning a Rust-only server.
    
    let addr_str = format!("{}:{}", host, port);
    let addr = match addr_str.parse::<SocketAddr>() {
        Ok(addr) => addr,
        Err(_) => return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid address format")),
    };

    // We need to ensure the Tokio runtime doesn't get dropped immediately if start_server returns.
    // One way is to spawn a thread that owns the runtime.
    // Or, for a simpler, potentially blocking call (if Python doesn't need to do anything else on this thread):
    // let rt = Runtime::new()?;
    // rt.block_on(run_rust_server_internal(addr));
    // This would block the Python caller.
    //
    // To run it in the background from Python's perspective:
    // We need a global runtime or to pass the runtime around, or use pyo3_asyncio.
    // Let's try spawning a new OS thread which will then create and run the Tokio runtime.
    // This is a common pattern for running a Rust server in the background when called from a synchronous FFI.
    
    // Using py.allow_threads to release the GIL, allowing the new thread to run concurrently.
    py.allow_threads(move || {
        std::thread::spawn(move || {
            let rt = match Runtime::new() {
                Ok(rt) => rt,
                Err(e) => {
                    eprintln!("Failed to create Tokio runtime: {}", e);
                    return;
                }
            };
            // Now block on the server future within this new thread.
            rt.block_on(run_rust_server_internal(addr));
        });
    });
    
    Ok(())
}
// --- End of PyO3 Exposed Functions ---

// --- PyO3 Module Definition ---
#[pymodule]
fn actixpy_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_hello, m)?)?;
    m.add_function(wrap_pyfunction!(start_server, m)?)?;
    Ok(())
}
// --- End of PyO3 Module Definition ---

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
