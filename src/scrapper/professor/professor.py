import httpx
from bs4 import BeautifulSoup


def fetch_single_professor(row) -> dict:
    link = row.select_one("a.nw-btn")["href"]
    name = row.select_one("big").text
    research_field = (
        row.select_one("span.rs").text.strip() if row.select_one("span.rs") else ""
    )

    detail_response = httpx.get(link)
    if detail_response.status_code == 200:
        detail_soup = BeautifulSoup(detail_response.text, "html.parser")
        contact_info = list(
            map(
                lambda x: x.text.strip(),
                detail_soup.select_one("div.info-wr ul").find_all("li"),
            )
        )

        email = contact_info[0] if len(contact_info) > 0 else ""
        tel = contact_info[1] if len(contact_info) > 1 else ""
        office = contact_info[2] if len(contact_info) > 2 else ""

        return {
            "username": name,
            "email": email,
            "tel": tel,
            "office": office,
            "research_field": research_field,
            "role": "PROFESSOR",
            "password": "test_password",
            "is_super": False,
        }
    else:
        print(
            f"Failed to fetch details for {name}. Status code: {detail_response.status_code}"
        )


def post_single_user(data: dict) -> int:
    response = httpx.post("http://localhost:8080/api/users", json=data)
    if response.status_code == 201:
        return response.json().get("id")
    else:
        print(
            f"Failed to post user data for {data['username']}. Status code: {response.status_code}"
        )
        return -1


def post_single_professor(data: dict, user_id: int) -> None:
    response = httpx.post(
        "http://localhost:8080/api/professors",
        json={
            "user_id": user_id,
            "position": data["role"],
            "office": data["office"],
            "tel": data["tel"],
            "research_field": data["research_field"],
            "appointed_at": 1,
        },
    )
    if response.status_code != 201:
        print(
            f"Failed to post professor data for {data['username']}. Status code: {response.status_code}"
        )

    else:
        print(f"Successfully posted data for {data['username']}.")


def post_professors():
    url = "https://computer.knu.ac.kr/bbs/board.php?bo_table=sub2_1"

    big_response = httpx.get(url)
    if big_response.status_code == 200:
        soup = BeautifulSoup(big_response.text, "html.parser")

        for row in soup.select("li.flip-box"):
            professor_data = fetch_single_professor(row)

            user_id = post_single_user(professor_data)
            if user_id == -1:
                print(f"Failed to post user data for {professor_data['username']}.")
            else:
                post_single_professor(professor_data, user_id)

    else:
        print(f"Failed to fetch the main page. Status code: {big_response.status_code}")


if __name__ == "__main__":
    post_professors()
