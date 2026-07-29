import json
from typing import Any

from src.models.generic_postgresql import GenericPostgresql


class ChatSessionContextRepository(GenericPostgresql):
	TABLE_NAME = "chat_session_context"

	def ensure_table(self) -> None:
		conn = self.get_connection()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
					f"""
					CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
						platform TEXT NOT NULL,
						tenant_id TEXT NOT NULL,
						locale TEXT NOT NULL,
						store_code TEXT NOT NULL,
						chat_session_id TEXT NOT NULL,
						context_json JSONB NOT NULL,
						updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
						PRIMARY KEY (platform, tenant_id, locale, store_code, chat_session_id)
					)
					"""
				)
				conn.commit()
		finally:
			conn.close()

	def load_context(
		self,
		platform: str,
		tenant_id: str,
		locale: str,
		store_code: str,
		chat_session_id: str,
	) -> dict[str, Any] | None:
		conn = self.get_connection()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
					f"""
					SELECT context_json
					FROM {self.TABLE_NAME}
					WHERE platform = %s
					  AND tenant_id = %s
					  AND locale = %s
					  AND store_code = %s
					  AND chat_session_id = %s
					""",
					(platform, tenant_id, locale, store_code, chat_session_id),
				)
				row = cursor.fetchone()
				if row is None:
					return None

				value = row[0]
				if isinstance(value, dict):
					return value
				if isinstance(value, str):
					try:
						parsed = json.loads(value)
						return parsed if isinstance(parsed, dict) else None
					except Exception:
						return None
				return None
		finally:
			conn.close()

	def save_context(
		self,
		platform: str,
		tenant_id: str,
		locale: str,
		store_code: str,
		chat_session_id: str,
		context: dict[str, Any],
	) -> None:
		conn = self.get_connection()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
					f"""
					INSERT INTO {self.TABLE_NAME} (
						platform, tenant_id, locale, store_code, chat_session_id, context_json, updated_at
					) VALUES (%s, %s, %s, %s, %s, %s::jsonb, now())
					ON CONFLICT (platform, tenant_id, locale, store_code, chat_session_id)
					DO UPDATE SET context_json = EXCLUDED.context_json, updated_at = now()
					""",
					(
						platform,
						tenant_id,
						locale,
						store_code,
						chat_session_id,
						json.dumps(context),
					),
				)
				conn.commit()
		finally:
			conn.close()

	def reset_context(
		self,
		platform: str,
		tenant_id: str,
		locale: str,
		store_code: str,
		chat_session_id: str,
	) -> None:
		conn = self.get_connection()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
					f"""
					DELETE FROM {self.TABLE_NAME}
					WHERE platform = %s
					  AND tenant_id = %s
					  AND locale = %s
					  AND store_code = %s
					  AND chat_session_id = %s
					""",
					(platform, tenant_id, locale, store_code, chat_session_id),
				)
				conn.commit()
		finally:
			conn.close()
