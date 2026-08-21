
# --- Stage 1: Build Stage (JDK + Maven) ---

FROM maven:3.9-eclipse-temurin-17-alpine AS builder
WORKDIR /app

# 1. Cache Maven dependencies first

COPY pom.xml .
RUN mvn dependency:go-offline


# 2 Copy the source code and build the application JAR

COPY src ./src
RUN mvn package -DskipTests


# --- Stage 2: Runtime Stage (Minimal JRE) ---

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Create non root system user for system security

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser


# Copy ONLY the compiled .jar artifact from Stage 1
COPY --from=builder /app/target/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
