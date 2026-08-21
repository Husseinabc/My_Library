from member import Member


def test_member_is_created_correctly():
    # ننشئ عضوًا جديدًا
    member = Member(
        1,
        "Ahmed",
        "0500000000",
        "ahmed@example.com"
    )

    # نتأكد أن بيانات العضو حُفظت بشكل صحيح
    assert member.member_id == 1
    assert member.name == "Ahmed"
    assert member.phone_number == "0500000000"
    assert member.email == "ahmed@example.com"