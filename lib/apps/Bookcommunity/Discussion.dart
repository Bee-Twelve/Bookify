// To parse this JSON data, do
//
//     final discussion = discussionFromJson(jsonString);

import 'dart:convert';

List<Discussion> discussionFromJson(String str) => List<Discussion>.from(json.decode(str).map((x) => Discussion.fromJson(x)));

String discussionToJson(List<Discussion> data) => json.encode(List<dynamic>.from(data.map((x) => x.toJson())));

class Discussion {
  String model;
  int pk;
  Fields fields;

  Discussion({
    required this.model,
    required this.pk,
    required this.fields,
  });

  factory Discussion.fromJson(Map<String, dynamic> json) => Discussion(
    model: json["model"],
    pk: json["pk"],
    fields: Fields.fromJson(json["fields"]),
  );

  Map<String, dynamic> toJson() => {
    "model": model,
    "pk": pk,
    "fields": fields.toJson(),
  };
}

class Fields {
  int user;
  int forum;
  String discuss;

  Fields({
    required this.user,
    required this.forum,
    required this.discuss,
  });

  factory Fields.fromJson(Map<String, dynamic> json) => Fields(
    user: json["user"],
    forum: json["forum"],
    discuss: json["discuss"],
  );

  Map<String, dynamic> toJson() => {
    "user": user,
    "forum": forum,
    "discuss": discuss,
  };
}
