const gen_query_btn = document.getElementById("generate_query_btn")
const run_query_btn = document.getElementById("run_query_btn");

const text_prompt_ta = document.getElementById("query_des");
const LOCAL_HOST = "http://127.0.0.1:5000";
const gen_query_ta = document.getElementById("generated_query");
const query_explanation = document.getElementById("explanation")

const table = document.getElementsByTagName("table")[0];
const table_body = document.getElementsByTagName("tbody")[0];
const table_head = document.getElementsByTagName("thead")[0];

const op_heading = document.getElementById("op_heading")
const els = document.getElementsByClassName("hidden")
const EXPECTED_OUTPUT = document.getElementById("expected_output")
const GENERATE_TEXT = document.getElementById("load_text")
const SPINNER = document.getElementById("spinner_btn")

let use_mongo;

const headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
};

const handle_mongo_output = (results) => {
    console.log(results)
    EXPECTED_OUTPUT.innerHTML = json_to_html(results)
}

async function is_mongo() {
    const res = await fetch(`${LOCAL_HOST}/is_mongo`, {
        method: "GET", // Send the use_mongo flag to the backend
        headers: headers
    });

    const results = await res.json();

    use_mongo = results["use_mongo"];
    console.log(use_mongo)

}
async function gen_query() {

    const text_prompt = text_prompt_ta.value;
     // Check if MongoDB is selected

    SPINNER.style.display = "block";
    gen_query_btn.style.display="none";


    const res = await fetch(`${LOCAL_HOST}/get_query`, {
        method: "POST",
        body: JSON.stringify({ text_prompt, use_mongo }),  // Send the use_mongo flag to the backend
        headers: headers
    });

    const results = await res.json();

    SPINNER.style.display = "none";
    gen_query_btn.style.display="block";

    console.log(results)

    for(const el of els)
        el.style.display = "block";
    
    gen_query_ta.value = results["gen_query"];
    gen_query_ta.focus();

    query_explanation.innerHTML = marked.parse(DOMPurify.sanitize(results["explanation"]));

    op_heading.innerHTML = "Expected Output of Query will be:";
    // table.style.display = "None";

    // EXPECTED_OUTPUT.innerHTML = marked.parse(DOMPurify.sanitize(results["table"]))
    console.log(results["table"])
    if (!use_mongo)
        update_table(results["table"]);
    else
        handle_mongo_output(JSON.parse(results["table"]));

}
const json_to_html = (obj) =>
{
    const br = "<br>"
    let html_str = "&emsp;["
    for (const doc of obj) {
        html_str+=br;
        html_str+=`&emsp;&emsp;{${br}`
        const entries = Object.entries(doc);
        const len_entries = entries.length;
        for(let idx  = 0 ; idx < len_entries; idx ++)
        {
           const field = entries[idx];

           if(idx != len_entries - 1)
                html_str+=`&emsp;&emsp;&emsp;${field[0]} : ${field[1]},`;
            else
            html_str+=`&emsp;&emsp;&emsp;${field[0]} : ${field[1]}`;
            html_str+=br;
        }
        html_str+=`&emsp;&emsp;},`
     
    }
    html_str+=`${br}&emsp;]`;
    return html_str;
}
gen_query_btn.addEventListener("click", gen_query);

async function run_query() {
    run_query_btn.blur()
    const query = gen_query_ta.value;
    const endpoint = '/run_query';  // Set the endpoint based on the toggle

    const res = await fetch(`${LOCAL_HOST}${endpoint}`, {
        method: "POST",
        body: JSON.stringify({ query , use_mongo}),  // Send the SQL/Mongo query
        headers: headers
    });

    const results = await res.json();

    op_heading.innerHTML = "Output of Query is:"
    if (use_mongo)
        handle_mongo_output(results["output"])
    else   
        update_table(results["output"]);  // Update the table with the query results
}

const empty_table = (element) => {
    while (element.hasChildNodes()) {
        element.removeChild(element.firstChild);
    }
};

const populate_table = (parent_el, results, el_type) => {
    for (const el_array of results) {
        const new_row = document.createElement("tr");
        for (const el of el_array) {
            const td = document.createElement(el_type);
            td.textContent = el;
            new_row.appendChild(td);
        }
        parent_el.appendChild(new_row);
    }
    const table = document.getElementsByTagName("table")[0];
    table.style.display = "block";
};

const update_table = (results) => {
    empty_table(table_head);
    empty_table(table_body);

    console.log([results[0]]);
    populate_table(table_head, [results[0]], "th");

    results.shift();
    populate_table(table_body, results, "td");
};

run_query_btn.addEventListener("click", run_query);


const animate_text = () =>
{
    if(GENERATE_TEXT.innerHTML === "Generating...")
        GENERATE_TEXT.innerHTML= "Generating&nbsp;&nbsp;&nbsp;"
    else
        GENERATE_TEXT.innerHTML = GENERATE_TEXT.innerHTML.replace("&nbsp;",".");

}

setInterval(animate_text,500);
window.onload = is_mongo;