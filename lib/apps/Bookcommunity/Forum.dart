// To parse this JSON data, do
//
//     final forum = forumFromJson(jsonString);

import 'dart:convert';

List<Forum> forumFromJson(String str) => List<Forum>.from(json.decode(str).map((x) => Forum.fromJson(x)));

String forumToJson(List<Forum> data) => json.encode(List<dynamic>.from(data.map((x) => x.toJson())));

class Forum {
  String model;
  int pk;
  Fields fields;

  Forum({
    required this.model,
    required this.pk,
    required this.fields,
  });

  factory Forum.fromJson(Map<String, dynamic> json) => Forum(
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
  String book;
  String subject;
  String description;
  DateTime dateCreated;

  Fields({
    required this.user,
    required this.book,
    required this.subject,
    required this.description,
    required this.dateCreated,
  });

  factory Fields.fromJson(Map<String, dynamic> json) => Fields(
    user: json["user"],
    book: json["book"],
    subject: json["subject"],
    description: json["description"],
    dateCreated: DateTime.parse(json["date_created"]),
  );

  Map<String, dynamic> toJson() => {
    "user": user,
    "book": book,
    "subject": subject,
    "description": description,
    "date_created": dateCreated.toIso8601String(),
  };
}
