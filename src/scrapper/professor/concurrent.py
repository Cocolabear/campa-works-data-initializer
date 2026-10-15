import httpx
from bs4 import BeautifulSoup


def fetch_single_professor(row) -> dict:
    name = row.select_one("div.txt-top p.name").text.strip().split()[0]
    office = row.select_one(".affiliation").text
    email = (
        row.select_one(".info-list li").text.strip()
        if row.select_one(".info-list li")
        else "."
    )
    research_field = (
        row.select_one("div.research").text if row.select_one("div.research") else "."
    )

    return {
        "name": name,
        "email": email,
        "tel": "no tel for invited professors",
        "office": office,
        "research_field": research_field,
        "role": "PROFESSOR",
        "password": "test_password",
        "position": "CONCURRENT",
    }


def post_single_user(data: dict) -> int:
    response = httpx.post("http://localhost:8080/api/users", json=data)
    if response.status_code == 201:
        return response.json().get("id")
    else:
        print(
            f"Failed to post user data for {data['name']}. Status code: {response.status_code}"
        )
        return -1


def post_single_professor(data: dict, user_id: int) -> None:
    response = httpx.post(
        "http://localhost:8080/api/professors",
        json={
            "user_id": user_id,
            "position": data["position"],
            "office": data["office"],
            "tel": data["tel"],
            "research_field": data["research_field"],
        },
    )
    if response.status_code != 201:
        print(
            f"Failed to post professor data for {data['name']}. Status code: {response.status_code}"
        )

    else:
        print(f"Successfully posted data for {data['name']}.")


def post_professors():
    url = "https://computer.knu.ac.kr/bbs/board.php?bo_table=sub2_3"

    big_response = httpx.get(url)
    if big_response.status_code == 200:
        soup = BeautifulSoup(big_response.text, "html.parser")

        for row in soup.select(".txt-wrap"):
            professor_data = fetch_single_professor(row)

            user_id = post_single_user(professor_data)
            if user_id == -1:
                print(f"Failed to post user data for {professor_data['name']}.")
            else:
                post_single_professor(professor_data, user_id)

    else:
        print(f"Failed to fetch the main page. Status code: {big_response.status_code}")


if __name__ == "__main__":
    post_professors()
