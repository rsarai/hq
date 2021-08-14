import { DateTime } from 'luxon';

export function fromMillisToDateHuge(milliseconds, timezone) {
  return fromMillisToDate(milliseconds, timezone).toLocaleString(
    DateTime.DATE_HUGE
  );
}

export function fromMillisToDateShort(milliseconds, timezone) {
  return fromMillisToDate(milliseconds, timezone).toLocaleString(
    DateTime.DATE_SHORT
  );
}

export function fromMillisToDate(milliseconds, timezone) {
  return DateTime.fromMillis(milliseconds, { zone: timezone }).setLocale('pt');
}

export function fromMillisToTimeSeconds(milliseconds, timezone) {
  return fromMillisToDate(milliseconds, timezone).toLocaleString(
    DateTime.TIME_24_WITH_SECONDS
  );
}

export function getDateFromEvent(event) {
  return fromMillisToDateShort(
    event.datetime.$date,
    event.timezone
  ).toLocaleString(DateTime.TIME_24_WITH_SECONDS);
}
